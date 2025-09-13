import sys
import asyncio
import platform
import logging
import csv
import argparse  # retained if future CLI flags are added (unused now)

# Local parser for AN9002 multimeter
from multimeter import *

# Matplotlib-only plotting configuration
PLOT_ENABLED = True
plt = None
_fig = _ax = _line = None

# Note: Avoid using the 'keyboard' library on Linux (requires root).
# Use Ctrl+C to stop the script instead.

try:
    from bleak import BleakClient
except Exception as e:
    # Let this raise at runtime if bleak truly missing; add hint for clarity.
    raise RuntimeError(
        "Bleak (BLE client) is not available. Install with 'pip install bleak'"
    ) from e

def setup_plot_backend():
    global plt, _fig, _ax, _line, PLOT_ENABLED
    if not PLOT_ENABLED:
        return
    try:
        import matplotlib.pyplot as _plt
        _plt.ion()
        fig, ax = _plt.subplots()
        line, = ax.plot([], [], color='b')
        ax.set_xlabel('Samples')
        plt = _plt
        _fig, _ax, _line = fig, ax, line
    except Exception as e:
        PLOT_ENABLED = False
        print(f"[info] Plotting disabled (matplotlib): {e}")

ADDRESS = (
    "9C:0C:35:FE:FC:55"
)

CHARACTERISTIC_UUID = "0000fff4-0000-1000-8000-00805f9b34fb"  # <--- Change to the characteristic you want to enable notifications from.

dataGraph = []
multimeter = AN9002()
lastDisplayedUnit = ""

def notification_handler(sender, data):
    global dataGraph
    global multimeter
    global lastDisplayedUnit
    """Simple notification handler which prints the data received."""
    #print("Data multimeter: {0}".format(data.hex(' ') ))
    multimeter.SetMeasuredValue(data)
    displayedData = multimeter.GetDisplayedValue()
    if multimeter.overloadFlag:
        displayedData = 99999
        print("Overload")

    unit = multimeter.GetDisplayedUnit()
    if lastDisplayedUnit == "":
        lastDisplayedUnit = unit
        if PLOT_ENABLED and _ax is not None:
            _ax.set_ylabel(unit)

    if unit != lastDisplayedUnit:
        lastDisplayedUnit = unit
        dataGraph.clear()
        if PLOT_ENABLED and _ax is not None:
            _ax.set_ylabel(unit)
            _line.set_data([], [])

    dataGraph.append(displayedData)
    print(str(displayedData) + " " + unit) 
     

async def run(address):
    client = BleakClient(address)
        
    try:
        await client.connect()
        await client.start_notify(CHARACTERISTIC_UUID, notification_handler)

        print("Connected. Press Ctrl+C to stop.")
        while True:
            if PLOT_ENABLED and plt is not None:
                _line.set_data(range(len(dataGraph)), dataGraph)
                _ax.relim()
                _ax.autoscale_view()
                plt.draw()
                plt.pause(0.1)
            await asyncio.sleep(0.5)

    except asyncio.CancelledError:
        # Graceful shutdown on Ctrl+C
        pass
    except Exception as e:
        print(e)
    finally:
        # Clean up only if connected; ignore errors on shutdown
        try:
            if getattr(client, 'is_connected', False):
                try:
                    await client.stop_notify(CHARACTERISTIC_UUID)
                except Exception:
                    pass
                try:
                    await client.disconnect()
                except Exception:
                    pass
        except Exception:
            pass


if __name__ == "__main__":
    # Matplotlib-only setup
    setup_plot_backend()

    # Use modern asyncio API to avoid DeprecationWarning on 3.11+
    asyncio.run(run(ADDRESS))

    with open('plot.csv', 'w') as f:
        wr = csv.writer(f)
        wr.writerow(dataGraph)
