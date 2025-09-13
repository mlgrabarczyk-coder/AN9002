This is a fortk form https://github.com/riktw/AN9002_info.

# AN9002 Bluetooth Multimeter Parser + Live Plot

This project reads measurements from an AN9002‑protocol Bluetooth multimeter, decodes the 7‑segment payload into numeric values/units, and shows a live plot using Matplotlib. A ready‑to‑run shell script bootstraps a Python 3.11 virtual environment and installs required packages.

## Contents
- `AN9002_pyton/multimeter.py` — AN9002 decoder. Converts raw notification bytes to a value and unit.
- `AN9002_pyton/ble_multimeter.py` — BLE client using `bleak`. Subscribes to notifications, decodes values, and plots them live with Matplotlib.
- `run_ble.sh` — One‑step runner that creates a venv (`.venv311` inside `AN9002/`), installs deps, and launches the reader.

## Requirements
- Python 3.11
- Bluetooth stack (BlueZ on Linux) with BLE support
- Python packages: `bleak`, `matplotlib` (installed automatically by `run_ble.sh`)

## Quick Start
From the repo root:

- Run: `bash AN9002/run_ble.sh`
- Stop: press Ctrl+C
- Output: values are plotted live; a `plot.csv` file is written on exit with the captured data points.

## Configuration
- Device address: edit `ADDRESS` in `AN9002_pyton/ble_multimeter.py` (default is a placeholder MAC).
- Characteristic UUID: update `CHARACTERISTIC_UUID` if your device uses a different notification UUID.

## How It Works
- Notifications are received via `bleak` and passed to `AN9002.SetMeasuredValue()`.
- The decoder interprets four 7‑segment digits, sign, and scaling flags to produce the displayed value and unit (V, mV, A, mA, Ω, kΩ, MΩ, Hz, F, etc.).
- Live plot uses a persistent Matplotlib line for efficient updates.

## Troubleshooting
- Device not found: confirm the MAC, turn on the multimeter, make sure it’s advertising and not paired elsewhere.
- Permissions: on Linux, you may need to be in the `bluetooth` group or run from a session with BLE access.
- Plotting disabled: if Matplotlib cannot import for your interpreter, use the provided venv by running the script via `run_ble.sh`.

## Manual Setup (optional)
If you prefer manual steps:

```
cd AN9002
python3.11 -m venv .venv311
source .venv311/bin/activate
pip install --upgrade pip
pip install matplotlib bleak
python AN9002_pyton/ble_multimeter.py
```

## Notes
- Quit with Ctrl+C; the script handles graceful shutdown and writes the CSV.
- The code is intentionally small and dependency‑light to keep it easy to adapt to related ANxxxx devices.
