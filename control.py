# control.py
from sensors import *
from actuators import *
from config import *

# -------------------------------------------------
# GLOBAL STATE (PERSISTENT)
# -------------------------------------------------
state = {
    "occupied": False,
    "light": 0,
    "temperature": 0,

    "lighting_on": False,
    "heating_on": False,
    "cooling_on": False,

    # Override flags
    "lighting_override": False,
    "heating_override": False,
    "cooling_override": False
}


# -------------------------------------------------
# MAIN UPDATE FUNCTION
# -------------------------------------------------
def update_system():

    # Read sensors
    state["occupied"] = read_occupancy()
    state["light"] = read_light()
    state["temperature"] = read_temperature()

    print("Occupied:", state["occupied"])

    # -------------------------------------------------
    # AUTOMATIC CONTROL (ONLY IF NOT OVERRIDDEN)
    # -------------------------------------------------

    # Lighting
    if not state["lighting_override"]:
        state["lighting_on"] = (
            state["occupied"] and state["light"] < LIGHT_THRESHOLD
        )

    # Heating
    if not state["heating_override"]:
        state["heating_on"] = (
            state["occupied"] and state["temperature"] < HEAT_SETPOINT
        )

    # Cooling
    if not state["cooling_override"]:
        state["cooling_on"] = (
            state["occupied"] and state["temperature"] > COOL_SETPOINT
        )

    # -------------------------------------------------
    # APPLY ACTUATORS (SINGLE SOURCE OF TRUTH)
    # -------------------------------------------------
    lighting(state["lighting_on"])
    heating(state["heating_on"])
    cooling(state["cooling_on"])

    return state

