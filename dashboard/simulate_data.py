# Testing file to test the imu and sensor readings with the dashboard

import paho.mqtt.client as mqtt
import json
import time
import random
import threading  # Required to run both loops of imu and sensor sims simultaneously

# Configuration
BROKER = "xxx.xxx.x.xx"  # Use your laptop's local IP here
PORT = 1883
TOPIC = "mars/telemetry"  # Or any other topic name, use the same topic to check on MQTT Explorer

client = mqtt.Client()


# Function to simulate IMU data
def simulate_imu():
    # Using a separate connection for this thread to avoid collisions
    imu_client = mqtt.Client()
    imu_client.connect(BROKER, PORT, 60)

    print(f"Virtual Cubesat connected to {BROKER}. Sending telemetry...")

    # Starting angles
    p, r, y = 0, 0, 0

    while True:
        # Simulate slight tilting of cubesat (Replace this with actual MPU6050 sensor data)
        p += random.uniform(-2, 2)
        r += random.uniform(-2, 2)
        y += random.uniform(-1, 1)

        # Payload packet includes:
        payload = {
            "pitch": round(p % 360, 2),
            "roll": round(r % 360, 2),
            "yaw": round(y % 360, 2),
        }

        # Publish data to MQTT Topic, so that dashboard can retrieve it
        imu_client.publish(TOPIC, json.dumps(payload))
        print(
            f"Sent Orientation: P:{payload['pitch']} R:{payload['roll']} Y:{payload['yaw']}"
        )
        time.sleep(0.05)  # Higher frequency for smooth 3D movement (20Hz)


# Function to simulate sensor data
def simulate_sensors():
    sensor_client = mqtt.Client()
    sensor_client.connect(BROKER, PORT, 60)
    print(f"Virtual Ground Station connected to {BROKER}. Sending telemetry...")

    # Base values for simulation
    temp = 22.0

    while True:
        # Generate random sensor data
        temp += random.uniform(-0.5, 0.5)
        light = random.randint(300, 800)
        vibration = 1 if random.random() > 0.9 else 0  # To give 10% chance of tremor

        # Simulate Dust Storm
        # We'll trigger an alarm if a random is very high
        dust_storm = True if random.random() > 0.95 else False

        payload = {
            "temp": round(temp, 2),  # Temperature (DHT)
            "light": light,  # Light intensity data (LDR)
            "vib": vibration,  # Vibration data (Vibration sensor)
            "dust_storm": dust_storm,  # If there is an incoming dust storm
        }

        # Publish data to MQTT Topic, so that dashboard can retrieve it
        message = json.dumps(payload)
        sensor_client.publish(TOPIC, message)

        status = "⚠️ ALARM!" if dust_storm else "Normal"
        print(f"Published: {message} | Status: {status}")

        time.sleep(1)  # Send data every second, slower rate of refresh than IMU data


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
