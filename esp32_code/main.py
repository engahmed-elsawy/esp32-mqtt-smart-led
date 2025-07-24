import machine
import time
import network
import ubinascii
from umqtt.simple import MQTTClient

# Wi-Fi configuration
SSID = "Wokwi-GUEST"
PASSWORD = ""
MQTT_BROKER = "broker.hivemq.com"
CLIENT_ID = ubinascii.hexlify(machine.unique_id())

# GPIO setup
relay_pin = machine.Pin(2, machine.Pin.OUT)     # GPIO2 controls the relay
temp_pin = machine.ADC(machine.Pin(34))         # GPIO34 reads temperature (NTC)
temp_pin.atten(machine.ADC.ATTN_11DB)           # Full ADC range (0-3.3V)

# Initial state
mode = "auto"           # "auto" or "manual"
threshold = 35          # Default temperature threshold in °C

# Connect to Wi-Fi
def connect_wifi():
    print("Connecting to WiFi...")
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    while not wlan.isconnected():
        time.sleep(0.2)
    print("WiFi connected:", wlan.ifconfig())

# Handle incoming MQTT messages
def on_message(topic, msg):
    global mode, threshold
    topic = topic.decode()
    msg = msg.decode()
    print("MQTT:", topic, "→", msg)
    
    if topic == "esp32/mode":
        if msg in ["auto", "manual"]:
            mode = msg
            print("Mode changed to:", mode)
    elif topic == "esp32/relay_cmd" and mode == "manual":
        if msg == "on":
            relay_pin.value(1)
        elif msg == "off":
            relay_pin.value(0)
    elif topic == "esp32/set_threshold":
        try:
            threshold = int(msg)
            print("Threshold set to:", threshold)
        except:
            print("Invalid threshold")

# Connect to MQTT broker
def mqtt_connect():
    client = MQTTClient(CLIENT_ID, MQTT_BROKER)
    client.set_callback(on_message)
    client.connect()
    client.subscribe(b'esp32/mode')
    client.subscribe(b'esp32/relay_cmd')
    client.subscribe(b'esp32/set_threshold')
    print("Connected to MQTT broker")
    return client

# Read simulated temperature from NTC
def read_temp():
    raw = temp_pin.read()  # 0 - 4095
    temp_c = (raw / 4095) * 100  # Approximate conversion to °C
    return int(temp_c)

# Main loop
connect_wifi()
client = mqtt_connect()

while True:
    client.check_msg()  # Listen for incoming MQTT messages

    temp = read_temp()
    print("Temp:", temp, "°C | Mode:", mode, "| Threshold:", threshold)
    
    # Publish current temperature to broker
    client.publish(b'esp32/temp', str(temp))

    # Automatic control logic
    if mode == "auto":
        if temp > threshold:
            relay_pin.value(1)
        else:
            relay_pin.value(0)

    time.sleep(2)

