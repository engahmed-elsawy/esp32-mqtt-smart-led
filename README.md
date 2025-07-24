# ESP32 Smart LED Control System via MQTT

## Overview

ESP32 reads temperature via an NTC thermistor and controls a relay-connected LED in two modes:

- **Auto Mode:** Relay turns on if temp > threshold, otherwise off.
- **Manual Mode:** LED/relay can be controlled remotely via MQTT commands.

## Setup

### ESP32 (MicroPython)
- Copy `esp32_code/main.py` to your ESP32.
- Connect hardware:
  - NTC thermistor + 10kΩ resistor as voltage divider to GPIO34.
  - Relay module to GPIO2 (and LED between NO–COM).
- Run code. Open serial monitor to verify Wi-Fi and MQTT connectivity.

### PC (Python)
- Install dependencies: `pip install paho-mqtt`
- Run with `python mqtt_controller.py`.
- Interact via menu to send mode, relay, and threshold commands.

## MQTT topics

- `esp32/temp` — publishes current temperature.
- `esp32/mode` — set operation mode (`auto` or `manual`).
- `esp32/relay_cmd` — send relay commands (`on` / `off`).
- `esp32/set_threshold` — update temperature threshold.

---

Feel free to clone, modify, and expand the project!
