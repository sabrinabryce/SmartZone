# test.py
"""
Quick Calibration Tool

Run in shell:
import test
test.run()
"""
import utime
from machine import ADC
from config import PIN_LIGHT, PIN_OCCUPANCY
from sensors import read_temperature

light_adc = ADC(PIN_LIGHT)
occ_adc = ADC(PIN_OCCUPANCY)


def capture_average(adc):

    total = 0
    samples = 30

    for i in range(samples):
        total += adc.read_u16()
        utime.sleep(0.05)

    return int(total / samples)


def run():

    print("\nSMARTZONE SENSOR CALIBRATION\n")

    print("Live readings running.")
    print("Press ENTER when ready to capture a value.\n")

    # -------------------------
    # live monitoring
    # -------------------------

    while True:

        light = light_adc.read_u16()
        occ = occ_adc.read_u16()

        print(
            "Light RAW:", light,
            "| Occ RAW:", occ,
            "| Temp:", read_temperature()
        )

        cmd = input("Press ENTER to start calibration or type c to continue: ")

        if cmd == "":
            break

    # -------------------------
    # DARK
    # -------------------------

    print("\nCover light sensor (DARK)")
    input("Press ENTER")
    dark = capture_average(light_adc)

    # -------------------------
    # ROOM LIGHT
    # -------------------------

    print("\nExpose to normal room light")
    input("Press ENTER")
    room = capture_average(light_adc)

    # -------------------------
    # FLASHLIGHT
    # -------------------------

    print("\nShine flashlight on sensor")
    input("Press ENTER")
    flash = capture_average(light_adc)

    # -------------------------
    # UNOCCUPIED
    # -------------------------

    print("\nLeave room empty")
    input("Press ENTER")
    empty = capture_average(occ_adc)

    # -------------------------
    # OCCUPIED
    # -------------------------

    print("\nStand in detection zone")
    input("Press ENTER")
    occupied = capture_average(occ_adc)

    # -------------------------
    # Calculate thresholds
    # -------------------------

    light_threshold = (dark + room) // 2
    occ_threshold = (empty + occupied) // 2

    # -------------------------
    # Print config values
    # -------------------------

    print("\n===== COPY INTO config.py =====\n")

    print("DARK_RAW =", dark)
    print("BRIGHT_RAW =", room)

    print("LIGHT_THRESHOLD =", light_threshold)

    print("\nOCC_THRESHOLD =", occ_threshold)

    print("\nReference values:")
    print("FLASH_LIGHT =", flash)
    print("UNOCCUPIED =", empty)

    print("OCCUPIED =", occupied)
