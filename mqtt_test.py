#!/usr/bin/env python3
import time, paho.mqtt.client as mqtt

BROKER_IP = "192.168.1.26"        # ← your broker
TOPIC = "home/pi/cpu_temp_c"
INTERVAL_S = 30

def read_cpu_temp_c():
    with open("/sys/class/thermal/thermal_zone0/temp") as f:
        return round(int(f.read().strip()) / 1000.0, 1)

client = mqtt.Client()
client.connect(BROKER_IP, 1883, 60)
client.loop_start()

try:
    while True:
        t = read_cpu_temp_c()
        client.publish(TOPIC, str(t), qos=1, retain=True)
        time.sleep(INTERVAL_S)
except KeyboardInterrupt:
    pass
finally:
    client.loop_stop()
    client.disconnect()
