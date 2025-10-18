from ws2812 import WS2812
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

while True:
    for color in COLORS:
        led.pixels_fill(color)
        led.pixels_show()
        utime.sleep(0.2)

