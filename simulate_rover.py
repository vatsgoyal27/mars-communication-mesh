import paho.mqtt.client as mqtt
import json
import time
import random
import threading  # Required to run both loops at once

# Configuration
BROKER = "192.168.0.34"  # Or use your laptop's IP
PORT = 1883
TOPIC = "mars/telemetry"

client = mqtt.Client()


def simulate_imu():
    # Use a separate connection for this thread to avoid collisions
    imu_client = mqtt.Client()
    imu_client.connect(BROKER, PORT, 60)

    # Starting angles
    p, r, y = 0, 0, 0

    while True:
        # Simulate slight tilting (Replace this with actual MPU6050 sensor reading logic)
        p += random.uniform(-2, 2)
        r += random.uniform(-2, 2)
        y += random.uniform(-1, 1)

        payload = {
            "temp": 22.5,
            "light": 500,
            "vibe": 0,
            "ir_storm": False,
            "pitch": round(p % 360, 2),
            "roll": round(r % 360, 2),
            "yaw": round(y % 360, 2),
        }

        imu_client.publish(TOPIC, json.dumps(payload))
        print(
            f"Sent Orientation: P:{payload['pitch']} R:{payload['roll']} Y:{payload['yaw']}"
        )
        time.sleep(0.05)  # Higher frequency for smooth 3D movement (20Hz)


def simulate_sensors():
    sensor_client = mqtt.Client()
    sensor_client.connect(BROKER, PORT, 60)
    print(f"🚀 Virtual Rover connected to {BROKER}. Sending telemetry...")

    # Base values for simulation
    temp = 22.0

    while True:
        # 1. Generate fake sensor data
        temp += random.uniform(-0.5, 0.5)
        light = random.randint(300, 800)
        vibration = 1 if random.random() > 0.9 else 0  # 10% chance of tremor

        # 2. Simulate IR Dust Storm (Trigger every ~15 seconds for testing)
        # We'll trigger an alarm if a random roll is very high
        ir_storm = True if random.random() > 0.95 else False

        payload = {
            "temp": round(temp, 2),
            "light": light,
            "vibe": vibration,
            "ir_storm": ir_storm,
        }

        # 3. Publish to MQTT
        message = json.dumps(payload)
        sensor_client.publish(TOPIC, message)

        status = "⚠️ ALARM!" if ir_storm else "Normal"
        print(f"Published: {message} | Status: {status}")

        time.sleep(1)  # Send data every second


if __name__ == "__main__":
    try:
        # Create two threads
        thread_imu = threading.Thread(target=simulate_imu)
        thread_sensors = threading.Thread(target=simulate_sensors)

        # Start both threads
        thread_imu.start()
        thread_sensors.start()

        # Keep the main thread alive while background threads work
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping Mission Simulation.")
