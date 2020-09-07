import time
from rpi_ws281x import PixelStrip, Color

import colorsys
import math

# LED strip configuration:
STRIP_OPTIONS = {
    "num": 30,  # Number of LED pixels.
    "pin": 18,  # GPIO pin connected to the pixels (18 uses PWM!).
    # "pin": 10,  # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
    "freq_hz": 800000,  # LED signal frequency in hertz (usually 800khz)

    "dma": 10,  # DMA channel to use for generating signal (try 10)
    # True to invert the signal (when using NPN transistor level shift)
    "invert": False,
    "brightness": 20,  # Set to 0 for darkest and 255 for brightest
    "channel": 0,  # set to '1' for GPIOs 13, 19, 41, 45 or 53
    "strip_type": None,
    "gamma": None
}

WAIT_MS = 100

if __name__ == "__main__":
    # Create NeoPixel object with appropriate configuration.
    strip = PixelStrip(**STRIP_OPTIONS)
    # Intialize the library (must be called once before other functions).
    strip.begin()

    NUM = STRIP_OPTIONS["num"]
    t = 0
    try:
        while True:
            rgb_float_row = [colorsys.hsv_to_rgb(
                ((i+t*0.1) / NUM) % 1.0,
                1,
                max(-((i - t*0.05 ) % NUM) ** 2 / (6**2) + 1, 0)
            )
                for i in range(NUM)]
            rgb_row = [tuple(min(int(x * 256), 255) for x in rgb)
                       for rgb in rgb_float_row]

            for i in range(NUM):
                r, g, b = rgb_row[i]
                strip.setPixelColorRGB(i, r, g, b)
            strip.show()

            t += 1

    except KeyboardInterrupt:
        del(strip)
        raise
