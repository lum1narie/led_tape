import time
from rpi_ws281x import PixelStrip, Color

import colorsys
import math

# LED strip configuration:
STRIP_OPTIONS = {
    "num": 30,  # Number of LED pixels.
    "pin": 18,  # GPIO pin connected to the pixels (18 uses PWM).
    # "pin": 21,  # GPIO pin connected to the pixels (21 uses PCM).
    # "pin": 10,  # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
    "freq_hz": 800000,  # LED signal frequency in hertz (usually 800khz)

    "dma": 10,  # DMA channel to use for generating signal (try 10)
    # True to invert the signal (when using NPN transistor level shift)
    "invert": False,
    "brightness": 0x10,  # Set to 0 for darkest and 255 for brightest
    "channel": 0,  # set to '1' for GPIOs 13, 19, 41, 45 or 53
    "strip_type": None,
    "gamma": None
}

WAIT_MS = 20





if __name__ == "__main__":
    # Create NeoPixel object with appropriate configuration.
    strip = PixelStrip(**STRIP_OPTIONS)
    # Intialize the library (must be called once before other functions).
    strip.begin()

    start_time = time.time()

    try:
        while True:
            elapsed_time = time.time() - start_time

            # write procedure here



            time.sleep(WAIT_MS / 1000)

    except KeyboardInterrupt:
        blank(strip)
        del(strip)
        raise
