from hx711 import HX711
import RPi.GPIO as GPIO
import time

NEXT_BTN_PIN = 23
RESET_BTN_PIN = 24

GPIO.setmode(GPIO.BCM)
GPIO.setup(NEXT_BTN_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(RESET_BTN_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def init_hx711():
    hx711 = HX711(dout_pin=5, pd_sck_pin=6, gain_channel_A=64)
    hx711.reset()   # Before we start, reset the HX711 (not obligate)
    hx711.zero()
    hx711.set_scale_ratio(scale_ratio=400)
    return hx711


def get_weight(hx711):
    try:
        if GPIO.input(24) == 0:
            hx711.zero(5)
        weight = hx711.get_weight_mean(5)
        return max(0, int(weight))
    except:
        pass


def get_next_btn():
    if GPIO.input(NEXT_BTN_PIN) == 0:
        return True
    return False
