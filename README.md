# SmartZone
SmartZone: Occupancy-based HVAC and lighting system designed for energy-saving (UVic ENGR 120 Design Project).

## Overview

SmartZone integrates

- Occupancy detection
- Ambient light sensing
- Temperature sensing
- Automated heating
- Automated cooling
- Automated lighting
- Web-based monitoring interface

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

main.py       → System entry point  
control.py    → Core HVAC + lighting logic  
sensors.py    → Sensor readings  
actuators.py  → Output control  
wifi.py       → Access point + server  
web.py        → Web dashboard rendering  
log.py        → System state logging  
test.py       → Calibration utility  
config.py     → Thresholds and calibration  

---

## How To Run

1. Power device.
2. Connect to SmartZone WiFi access point.
3. Open browser to device IP address.
4. Dashboard updates automatically every 1 second.

---

## Calibration

To recalibrate in a new room open shell and run

    import test
    test.run()

Observe raw light, temperature, and occupancy values.

Then adjust

- BRIGHT_RAW
- DARK_RAW
- OCC_THRESHOLD
- HEAT_SETPOINT
- COOL_SETPOINT

in config.py.

Reboot system.

---

## Architecture

The system architecture is as follows:

Sensors → Control Logic → Actuators → Web Interface → Logging

Zone ID is configurable for future multi-zone deployment.

Currently configured for Zone 101.

