# SmartZone
SmartZone is an occupancy-based HVAC and lighting automation system built on a Raspberry Pi Pico W.

Developed for UVic ENGR 120 Design Project

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

The system is designed for multi-zone scalability.

---

## System Logic

Lighting:
- Turns ON when room is occupied AND ambient light is below threshold.

Heating:
- Turns ON when room is occupied AND temperature is below heat setpoint.

Cooling:
- Turns ON when room is occupied AND temperature is above cool setpoint.

Safety:
- Heating and cooling never run simultaneously. Manual overrides are provided. 

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

---

## How To Run

Start the system by running: main.py 

You will see the SmartZone menu: 
1: Run the system → Starts full system
2: Run debug mode → Runs system without logging and prints live data
3: Run testing → Runs sensor calibration tool (to update config.py) 

---

## Conecting to the Web Dashboard 

1. Power the device.
2. Connect to SmartZone WiFi access point: SMARTZONE_PICO.
3. Enter the WiFi password.
4. Open browser to device IP address (shown in console).
5. Enter the interface password.

---

## Architecture

The system architecture is as follows:

Sensors → Control Logic → Actuators → Web Interface → Logging

Zone ID is configurable for future multi-zone deployment.

Currently configured for Zone 101.

