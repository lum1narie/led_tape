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


def runner(strip, time,
           flow_speed=5.0,
           light_range=6.0,
           hue_duration=3.0,
           hue_loop=2.0,
           saturation=1.0):
    num = strip.numPixels()

    def phase(i): return ((flow_speed * time - i + num / 2) % num) - num / 2
    rgb_float_row = [
        colorsys.hsv_to_rgb(
            (time / hue_duration + i * hue_loop / num) % 1.0,
            saturation,
            ((math.cos(phase(i) * 2 * math.pi / light_range) + 1) / 2 
             if abs(phase(i)) <= (light_range / 2)
             else 0)
        )
        for i in range(num)
    ]
    rgb_row = [tuple(min(int(x * 256), 255) for x in rgb)
               for rgb in rgb_float_row]

    for i in range(num):
        r, g, b = rgb_row[i]
        strip.setPixelColorRGB(i, r, g, b)
    strip.show()


def hue_single(strip, time,
               hue_duration=5.0,
               saturation=1.0,
               ):
    num = strip.numPixels()

    rgb_float = colorsys.hsv_to_rgb(
        (time / hue_duration) % 1.0,
        saturation,
        1
    )
    rgb = tuple(min(int(x * 256), 255) for x in rgb_float)

    for i in range(num):
        r, g, b = rgb
        strip.setPixelColorRGB(i, r, g, b)
    strip.show()


def single(strip, color):
    num = strip.numPixels()
    for i in range(num):
        strip.setPixelColor(i, color)
    strip.show()


def sample_hue_saturation(strip, time, hue_duration=5.0):
    num = strip.numPixels()

    def phase(i): return (i - num / 2)
    rgb_float_row = [
        colorsys.hsv_to_rgb(
            (time / hue_duration) % 1.0,
            - ((phase(i)) / (num / 2)) ** 2 + 1.0,
            1
        )
        for i in range(num)
    ]
    rgb_row = [tuple(min(int(x * 256), 255) for x in rgb)
               for rgb in rgb_float_row]

    for i in range(num):
        r, g, b = rgb_row[i]
        strip.setPixelColorRGB(i, r, g, b)
    strip.show()


def blank(strip):
    single(strip, Color(0, 0, 0))


if __name__ == "__main__":
    # Create NeoPixel object with appropriate configuration.
    strip = PixelStrip(**STRIP_OPTIONS)
    # Intialize the library (must be called once before other functions).
    strip.begin()

    start_time = time.time()

    try:
        while True:
            elapsed_time = time.time() - start_time
            runner(strip, elapsed_time,
                   flow_speed=10.0,
                   hue_duration=-2.0,
                   light_range=8)
            time.sleep(WAIT_MS / 1000)

    except KeyboardInterrupt:
        blank(strip)
        del(strip)
        raise
