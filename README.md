# Mars Communication Mesh

**Rapid, Scalable Communication Infrastructure for Future Mars Exploration.**

![Project Status](https://img.shields.io/badge/Mission-Active-brightgreen)
![](https://img.shields.io/badge/Hardware-ESP32--C6-red)
![](https://img.shields.io/badge/Hardware-ESP32--C3-red)
---
### Note: For detailed info and schematics, look into the hosted Github pages site.
---
## 🛰️ Executive Summary
The **Mars Communication Mesh** is a modular, low-power communication infrastructure designed for early-stage and long-term exploration. By integrating **1U CubeSat relay nodes** with **intelligent ground-based safety hubs**, the system provides resilient, self-healing connectivity between astronauts, rovers, and surface habitats. Unlike traditional centralized systems, this distributed architecture prioritizes redundancy, energy efficiency, and rapid deployment in infrastructure-poor environments.


## 🚩 The Problem: The "Blackout" Isolation Crisis
A lethal **Information Gap plagues Mars exploration**. During catastrophic dust storms, traditional communication systems fail, and this mesh is designed to overcome such critical communication barriers:
* **Horizon Blindness:** Visual sensors are obscured by rising dust.
* **Signal Attenuation:** Local radio links are swallowed by atmospheric noise.
* **Mechanical Fatigue:** Fixed antennas cannot "hunt" for orbiting assets through the interference.
* **Infrastructure Risk:** Deploying fixed infrastructure is slow and expensive; failures during emergencies can result in loss of life.
* **Connectivity Gap:** There is currently no lightweight, rapidly deployable solution for inter-settlement connectivity.

## 🗼 Our Solution: The Lighthouse, Link, Hive architecture
We have engineered a **Predictive Safety Hub** that transforms a stationary base into a "Lighthouse" for the Martian frontier. By focusing on infrastructure over simple robotics, we solve the backbone challenges of space exploration.

## 🏗️ System Architecture: Lighthouse, Link & the Hive
1. **The Lighthouse** Remote patrol bases placed in the city periphery to detect a storm via **IR/LDR** sensors, gimbal skyward and "punches" an SOS through the dust to the **CubeSat**.
2. **The Link:** The CubeSat aligns itself to the ground stations (prevents tumbling using the custom-built magnetorquer), and beams the SOS to the main city
3. **The Hive:** The main city, the SOS from the CubeSat allows residents to seal airlocks and retract solar panels before the storm arrives.

---

### 1. The Predictive Alt-Azimuth Gimbal
Instead of power-hungry signal sweeping, the station runs a synchronized **Orbit Propagator**. (Orbit Propagator mechanism will be integrated soon)
* **Zero-Latency Alignment:** The **ESP32-C6** (base station) pre-calculates the CubeSat’s trajectory.
* **Kinematic Precision:** A dual-axis **Alt-Azimuth gimbal** slews the antenna to intercept the CubeSat before it even rises.

### 2. The Safety Hub (Sensors)
The station monitors four critical vectors to ensure mission safety:
* **Dust Opacity (IR):** Measures transparency to trigger emergency alerts.
* **Solar Flux (LDR):** Tracks solar intensity to confirm orbital visibility.
* **Tremors (Vibration/Tilt sensor):** Solder-mounted to detect ground stability and mechanical motor health.
* **Temperature (DHT22 sensor):** Monitors ambient temperature


### 3. PCB-Integrated Patch Antenna
To eliminate fragile external assemblies, the system uses a **microstrip patch antenna** integrated directly into the PCB.
* **Directional Gain:** Concentrates energy normal to the patch surface to improve link efficiency.

---

## 📊 Telemetry & Link Budget
A rigorous **Link Budget Analysis** ensures communication reliability under worst-case Mars conditions. 
* **Transmit Power ($P_t$):** 15 dBw.
* **Frequency:** 433 MHz (UHF band).
* **Link Margin:** Calculated using MATLAB to maintain signal strength above receiver sensitivity even with propagation and atmospheric losses.

---

## 💻 Mission Control Dashboard
A real-time telemetry interface provides high-contrast monitoring for rapid decision-making:
* **3D Visualization:** Displays CubeSat orientation (pitch, roll, yaw) at 20 Hz using **MPU6050 IMU** data.
* **Environmental Logs:** Time-series plots for temperature and luminosity updated at 1 Hz.
* **Emergency Latches:** Persistent alert panels for seismic activity or dust-induced signal loss.

---

## 🏁 Impact & Vision
The Mars Communication Mesh enables **reliable emergency response**, resource coordination, and continuous connectivity. Beyond technical utility, the system supports **human morale and safety** by ensuring astronauts are never completely isolated. In the long term, this mesh network serves as a foundational layer for Martian settlements, expanding organically as new nodes are deployed.

### 🛠️ Tech Stack
* **Microcontrollers:** ESP32-C6, ESP32-C3
* **Communication:** MQTT, BLE, Wi-Fi 6
* **Design Tools:** Fusion, KiCad, CST

## 📟 Pin Mapping (ESP32-C6)
| Component | Pin | Type | Logic / Role |
| :--- | :--- | :--- | :--- |
| **LDR** | **GPIO 0** | Analog (ADC1) | Light intensity tracking |
| **Vibration** | **GPIO 2** | Analog (ADC1) | Seismic/Mechanical health |
| **DHT Sensor** | **GPIO 9** | Digital | Thermal monitoring |
| **IR Sensor** | **GPIO 1** | Digital | Storm opacity trigger |
| **Altitude Servo**| **GPIO 19** | PWM | Precision altitude tracking |
| **Azimuth Servo** | **GPIO 18** | PWM | Precise base rotation |

---

## 🏁 How to Use
1. Clone the repository
   ```git clone https://github.com/vatsgoyal27/mars-communication-mesh.git```
2. Update the various code file inits with your SSID, PASSWORD, and your system's Local IP. (To use MQTT, Wifi)
3. Ensure you have a software like MQTT Explorer installed to check the data being published to the port specified in the code.
4. ```pip install``` all the required libraries in the code.
5. **Flash:** Upload the firmware in the directory ```ground``` to the **GLYPH C6** (ground station) and the files in the directory ```satellite``` to the **ESP32-C3** using ESP-IDF or Arduino IDE.
6. Ensure that the file ```C:\Program Files\mosquitto\mosquitto.conf``` has the following content at the top of it:
   ```
      # Standard connection for Python/MQTT Explorer
      listener 1883
      protocol mqtt

      # WebSocket connection for the Web Dashboard
      listener 9001
      protocol websockets
      allow_anonymous true
   ```
7. Start the MQTT server using ```mosquitto -c "C:\Program Files\mosquitto\mosquitto.conf" -v```
8. Execute the file ```main.py``` of both the ```ground``` and ```satellite``` using an editor like **Thonny**.
9. You should see live sensor data being pushed to the MQTT port on your MQTT Explorer.
10. You can host the ```dashboard.html``` file on a local webserver, connected to the same MQTT port to see it being updated with live sensor and IMU data.

---

> *"We aren't just building a radio; we are building Planetary Infrastructure. The Lighthouse hears the storm, pre-calculates the lifeline, and ensures the Hive survives."*
---

**Contributors:**
*[Yog](https://www.linkedin.com/in/yog-panjarale) • [Shreyas](https://www.linkedin.com/in/shreyas-cheruku-071a17324/) • [Vatsal](https://www.linkedin.com/in/vatsal-goyal-144659309/) • [Sreekar](https://www.linkedin.com/in/sai-sreekar-0823a91b0/)*
