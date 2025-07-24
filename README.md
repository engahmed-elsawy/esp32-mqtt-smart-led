# 🔌 ESP32 Smart LED Control System via MQTT

## 🌡️ Overview
This project uses an **ESP32** to monitor temperature via an **NTC thermistor** and control a **relay-connected LED** in two operating modes:

- **🔁 Auto Mode**:  
  - The relay (and LED) turns **ON** if the temperature exceeds a defined threshold.  
  - Turns **OFF** when temperature drops below the threshold.

- **🎮 Manual Mode**:  
  - The relay can be turned **ON/OFF remotely** using MQTT commands from a PC or another client.

---

## 🔧 Setup

### 📱 ESP32 (MicroPython)

1. Copy `esp32_code/main.py` to your ESP32.
2. Connect hardware:
   - **NTC Thermistor** + 10kΩ resistor as a voltage divider → **GPIO34**
   - **Relay Module** control pin → **GPIO2**
   - LED connected between **NO–COM** on the relay
3. Run the code.
4. Open the **Serial Monitor** to verify:
   - Wi-Fi connection
   - MQTT broker connectivity

---

### 💻 PC (Python MQTT Controller)

1. Install required library:
   ```bash
   pip install paho-mqtt


---

Feel free to clone, modify, and expand the project!
