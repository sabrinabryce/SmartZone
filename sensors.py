# sensors.py
import machine
import math
import utime
from config import *

# ADC setup
adc_temp = machine.ADC(PIN_THERMISTOR)
adc_light = machine.ADC(PIN_LIGHT)
adc_occ = machine.ADC(PIN_OCCUPANCY)

# Thermistor constants
KELVIN = 273.15
BETA = 3960
T0 = 298.15  # 25°C in Kelvin

def read_temperature():
    raw = adc_temp.read_u16()
    if raw <= 0 or raw >= 65535:
        return None

    R0 = 10000  # 10k fixed resistor
    resistance = R0 * raw / (65535 - raw)

    temp_k = 1 / (1/T0 + (1/BETA) * math.log(resistance / R0))
    temp_c = (temp_k - KELVIN) * TEMP_SCALE

    # DEBUG
    print("Temp: ", temp_c, "C")
    
    return round(temp_c, 1)

def read_light():
    raw = adc_light.read_u16()

    # Clamp to calibrated range
    if raw < BRIGHT_RAW:
        raw = BRIGHT_RAW
    if raw > DARK_RAW:
        raw = DARK_RAW

    # Scale so:
    # Bright (15000) → 0%
    # Dark   (60000) → 100%
    percent = (DARK_RAW - raw) * 100 / (DARK_RAW - BRIGHT_RAW)
    
    # DEBUG
    print("Light level:", percent, " %")
    return int(percent)

def read_occupancy():
    value = adc_occ.read_u16()
    
    # DEBUG 
    print("Occ raw:", value)
    
    return value > OCC_THRESHOLD

