# actuators.py
import machine
from config import *

led_heat = machine.Pin(PIN_LED_HEAT, machine.Pin.OUT)
led_light = machine.Pin(PIN_LED_LIGHT, machine.Pin.OUT)
led_cool = machine.Pin(PIN_LED_COOL, machine.Pin.OUT)
ir_led = machine.Pin(PIN_IR_LED, machine.Pin.OUT)

def lighting(on):
    led_light.value(1 if on else 0)

def heating(on):
    led_heat.value(1 if on else 0)

def cooling(on):
    led_cool.value(1 if on else 0)

def ir_emitter(on=True):
    ir_led.value(1 if on else 0)
