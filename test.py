# test.py
"""
Quick Calibration Tool
Run in shell:

import test
test.run()

Ctrl+C to exit.
"""

import utime
from sensors import read_light, read_temperature, read_occupancy
from machine import ADC
from config import PIN_LIGHT

adc = ADC(PIN_LIGHT)

def run():
    print("\n=== SMARTZONE CALIBRATION MODE ===")
    print("Ctrl+C to exit\n")

    try:
        while True:
            raw_light = adc.read_u16()

            print("Raw Light:", raw_light,
                  "| Brightness %:", read_light(),
                  "| Temp °C:", read_temperature(),
                  "| Occupied:", read_occupancy())

            utime.sleep(0.1)

    except KeyboardInterrupt:
        print("\nCalibration ended.")