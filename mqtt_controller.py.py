import paho.mqtt.client as mqtt

BROKER = "broker.hivemq.com"
TEMP_TOPIC = "esp32/temp"
MODE_TOPIC = "esp32/mode"
CMD_TOPIC = "esp32/relay_cmd"
THRESHOLD_TOPIC = "esp32/set_threshold"

def on_connect(client, userdata, flags, rc):
    print("Connected with result code", rc)
    client.subscribe(TEMP_TOPIC)

def on_message(client, userdata, msg):
    print(f"[{msg.topic}] → {msg.payload.decode()} °C")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(BROKER, 1883, 60)
client.loop_start()

try:
    while True:
        print("\nOptions:")
        print("1. Set Mode (auto/manual)")
        print("2. Send Relay Command (on/off)")
        print("3. Set Temperature Threshold")
        choice = input("Choose (1/2/3): ").strip()
        if choice == "1":
            mode = input("Enter mode (auto/manual): ").strip().lower()
            client.publish(MODE_TOPIC, mode)
        elif choice == "2":
            cmd = input("Enter relay command (on/off): ").strip().lower()
            client.publish(CMD_TOPIC, cmd)
        elif choice == "3":
            th = input("Enter new threshold (e.g. 40): ").strip()
            client.publish(THRESHOLD_TOPIC, th)
        else:
            print("Invalid option.")
except KeyboardInterrupt:
    print("Exiting.")
    client.loop_stop()
    client.disconnect()
