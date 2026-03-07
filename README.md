# SmartZone
Occupancy-Based HVAC and Lighting Automation System  
Built on a **Raspberry Pi Pico W**

Developed for the **UVic ENGR 120 Design Project**

![Platform](https://img.shields.io/badge/platform-Raspberry%20Pi%20Pico%20W-7b68ee)
![Language](https://img.shields.io/badge/language-MicroPython-da70d6)
![Project](https://img.shields.io/badge/project-ENGR120-5dade2)

## System Overview

SmartZone demonstrates automatic control of building zones using sensor data. 

Sensors include the following: 

- IR Beam-Break Occupancy Detector
- Ambient Light Sensor
- Temperature (Thermistor) 

Based on these inputs, SmartZone controls the following: 

- Lighting
- Heating
- Cooling

The web dashboard allows users to 
- Monitor live zone status
- Apply manual overrides
- Visualize zone occupancy 

---

# System Logic

### Lighting

Turns **ON** when:

- The room is occupied AND Ambient light is below the configured threshold

### Heating

Turns **ON** when:

- The room is occupied AND Temperature is below the heating setpoint

### Cooling

Turns **ON** when:

- The room is occupied AND Temperature is above the cooling setpoint

### Safety

- Heating and cooling never run simultaneously
- Manual overrides are available from the web interface

---

# Running the System

Start the system by running:


main.py


The SmartZone menu will appear:


1: Run the system

2: Run debug mode

3: Run testing


### Option 1: Run the System

Starts the full SmartZone system.

Features:

- Automatic HVAC and lighting control
- Web interface dashboard
- Data logging

### Option 2: Debug Mode

Runs the system **without logging** and prints live sensor data to the console.

Useful for:

- Testing sensors
- Debugging thresholds

### Option 3: Testing Mode

Runs the **sensor calibration tool**.

This tool measures environmental values and provides recommended configuration values to update in `config.py`.

---

## Conecting to the Web Dashboard 

1. Power the device.
2. Connect to SmartZone WiFi access point: SMARTZONE_PICO.
3. Enter the WiFi password.
4. Open browser to device IP address (shown in console).
5. Enter the interface password.

---

## File Structure

main.py       → System entry point and menu 

control.py    → Core HVAC + lighting logic 

sensors.py    → Sensor readings  

actuators.py  → Output control  

wifi.py       → Access point + server  

web.py        → Web dashboard rendering  

log.py        → System state logging  

test.py       → Calibration tool  

config.py     → Thresholds and calibration values

Sensors → Control Logic → Actuators → Web Interface → Logging

---

# Scalability

The system is designed to support **multiple zones**.

Each zone can be assigned a unique `ZONE_ID` in `config.py`.

Current configuration:


Zone 101
