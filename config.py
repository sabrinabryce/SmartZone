# config.py
import machine

# ----------------
# WIFI CONFIG
# ----------------

AP_SSID = "SMARTZONE_PICO"
AP_PASSWORD = "smartzone"

# ----------------
# WEB CONFIG
# ----------------
ZONE_ID = "101"

# ----------------
# PIN DEFINITIONS
# ----------------

# --- ADC inputs ---
PIN_THERMISTOR = 26     # ADC0
PIN_LIGHT = 27          # ADC1
PIN_OCCUPANCY = 28      # ADC2

# --- Digital outputs ---
PIN_IR_LED = 16
PIN_LED_HEAT = 17
PIN_LED_LIGHT = 18
PIN_LED_COOL = 19

# ----------------
# SYSTEM SETTINGS
# ----------------

# --- TEMP CALIBRATION ---
TEMP_SCALE = 0.23
HEAT_SETPOINT = 20.0         # °C
COOL_SETPOINT = 24.0         # °C

# --- OCCUPANCY CALIBRATION ---
OCC_THRESHOLD = 52850 # threshold


# --- LIGHT CALIBRATION ---
BRIGHT_RAW = 50000   # normal room lighting
DARK_RAW = 60000     # fully covered
LIGHT_THRESHOLD = 60   # lights turn on when darker than 60%

