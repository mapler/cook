NEXT_BTN_PIN = 23
RESET_BTN_PIN = 24
HX711_SCALE = 370


class Device:

    def __init__(self, debug=False):
        self.debug = debug
        if not debug:
            print("Device init.")
            import RPi.GPIO as GPIO
            from hx711 import HX711
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(NEXT_BTN_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.setup(RESET_BTN_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            self.hx711 = HX711(dout_pin=5, pd_sck_pin=6, gain_channel_A=64)
            self.hx711.reset()   # Before we start, reset the HX711 (not obligate)
            self.hx711.zero()
            self.hx711.set_scale_ratio(scale_ratio=HX711_SCALE)
        else:
            print("Debug mode.")

    def get_weight(self):
        if not self.debug:
            try:
                import RPi.GPIO as GPIO
                if GPIO.input(RESET_BTN_PIN) == 0:
                    self.hx711.zero(5)
                weight = self.hx711.get_weight_mean(5)
                return int(weight)
            except:
                pass
        else:
            return 10

    def get_next_btn(self):
        if not self.debug:
            import RPi.GPIO as GPIO
            if GPIO.input(NEXT_BTN_PIN) == 0:
                return True
            return False
        else:
            return False
