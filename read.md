# SmartZone

Occupancy-Based HVAC and Lighting Automation System  
Built on a **Raspberry Pi Pico W**

Developed for the **UVic ENGR 120 Design Project**

![Platform](https://img.shields.io/badge/platform-Raspberry%20Pi%20Pico%20W-blue)
![Language](https://img.shields.io/badge/language-MicroPython-green)
![Project](https://img.shields.io/badge/project-ENGR120-orange)

---

# Quick Start

1. Power the Raspberry Pi Pico W
2. Run `main.py`
3. Select an option from the SmartZone menu
4. Connect to WiFi **SMARTZONE_PICO**
5. Open the device IP address in a browser
6. Enter the dashboard password

---

# System Overview

SmartZone demonstrates automatic control of building zones using sensor data.

Sensors include:

- IR Beam-Break Occupancy Detector
- Ambient Light Sensor
- Temperature Sensor (Thermistor)

Based on these inputs, SmartZone automatically controls:

- Lighting
- Heating
- Cooling

The web dashboard allows users to:

- Monitor live zone status
- Apply manual overrides
- Visualize zone occupancy

The system is designed for **multi-zone scalability**.

---

# System Logic

### Lighting

Turns **ON** when:

- The room is occupied  
AND  
- Ambient light is below the configured threshold

### Heating

Turns **ON** when:

- The room is occupied  
AND  
- Temperature is below the heating setpoint

### Cooling

Turns **ON** when:

- The room is occupied  
AND  
- Temperature is above the cooling setpoint

### Safety

- Heating and cooling never run simultaneously
- Manual overrides are available from the web interface

---

# System Architecture


IR Sensor
Light Sensor
Thermistor
│
▼
Control Logic
│
▼
Lighting / Heating / Cooling
│
▼
Web Dashboard + Logging


---

# File Structure


main.py System entry point and system menu
control.py Core HVAC and lighting control logic
sensors.py Sensor reading functions
actuators.py Hardware output control
wifi.py WiFi access point and web server
web.py Web dashboard interface
log.py System data logging
test.py Sensor calibration tool
config.py System configuration and thresholds


---

# Running the System

Start the system by running:


main.py


The SmartZone menu will appear:


1: Run the system
2: Run debug mode
3: Run testing


### Option 1 — Run the System

Starts the full SmartZone system.

Features:

- Automatic HVAC and lighting control
- Web interface dashboard
- Data logging

### Option 2 — Debug Mode

Runs the system **without logging** and prints live sensor data to the console.

Useful for:

- Testing sensors
- Debugging thresholds

### Option 3 — Testing Mode

Runs the **sensor calibration tool**.

This tool measures environmental values and provides recommended configuration values to update in `config.py`.

---

# Connecting to the Web Dashboard

1. Power the device
2. Connect to the WiFi access point:


SMARTZONE_PICO


3. Enter the WiFi password
4. Open a browser and go to the device IP address (shown in the console)
5. Enter the interface password

The dashboard will display:

- Zone occupancy
- Temperature
- Light level
- System status

Users can also apply **manual overrides** for lighting, heating, and cooling.

---

# Calibration

To calibrate sensors in a new environment run:


import test
test.run()


The calibration tool will measure:

- Light levels
- Occupancy thresholds
- Temperature readings

It will output recommended values to copy into `config.py`.

---

# Scalability

The system is designed to support **multiple zones**.

Each zone can be assigned a unique `ZONE_ID` in `config.py`.

Current configuration:


Zone 101
