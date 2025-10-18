from ws2812 import WS2812
from machine import Pin,ADC
import utime 

BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
WHITE = (255, 255, 255)
COLORS = [RED, GREEN, BLUE, YELLOW, CYAN, MAGENTA, WHITE]

led = WS2812(18, 1)
mic = ADC(Pin(27))  # Microphone sur A1 (GP27)

while True:
    mic_value = mic.read_u16()  # Lecture du micro en format u16 (0-65535)
    print("Valeur micro:", mic_value)
    utime.sleep(0.1)

