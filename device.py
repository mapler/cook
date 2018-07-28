from hx711 import HX711
import RPi.GPIO as GPIO
import time


def get_weight():
    try:
        hx711 = HX711(dout_pin=5, pd_sck_pin=6, gain_channel_A=64)
        hx711.reset()   # Before we start, reset the HX711 (not obligate)
        hx711.zero()
        hx711.set_scale_ratio(scale_ratio=400)
        measures = hx711.get_weight_mean(10)
    except:
        measures = 0
    finally:
        GPIO.cleanup()
    return max(0, measures)
