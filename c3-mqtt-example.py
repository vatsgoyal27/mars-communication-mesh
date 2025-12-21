import network
import time
from umqtt.simple import MQTTClient
import machine

# ================= WiFi =================
SSID = "Pixel_2085"
PASSWORD = "7736899422"

# ================= MQTT =================
MQTT_BROKER = "broker.mqtt.cool"
MQTT_PORT = 1883
TOPIC = b"hardwarehacka/team18"
CLIENT_ID = b"esp32c3_team18"

# ================= LED (optional) =================
led = machine.Pin(8, machine.Pin.OUT)

# ================= WiFi Connect =================
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if not wlan.isconnected():
        print("Connecting to WiFi...")
        wlan.connect(SSID, PASSWORD)

        while not wlan.isconnected():
            time.sleep(0.5)
            print(".", end="")

    print("\nWiFi connected")
    print("IP:", wlan.ifconfig()[0])
    led.on()

# ================= MQTT Connect =================
def connect_mqtt():
    print("Connecting to MQTT...")
    client = MQTTClient(
        CLIENT_ID,
        MQTT_BROKER,
        port=MQTT_PORT,
        keepalive=60
    )
    client.connect()
    print("MQTT connected")
    return client

# ================= Main =================
connect_wifi()
mqtt = connect_mqtt()

counter = 0

while True:
    try:
        msg = str(counter)
        print("Publishing:", msg)
        mqtt.publish(TOPIC, msg)
        counter += 1
        time.sleep(2)

    except Exception as e:
        print("Error:", e)
        led.off()
        time.sleep(3)
        machine.reset()

