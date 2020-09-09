import time
from rpi_ws281x import PixelStrip, Color

import colorsys
import math

import random

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


def light_ripples(strip, ripples):
    num = strip.numPixels()

    rgb_row = [[0, 0, 0] for _ in range(num)]
    for rp in ripples:
        c = rp["color"]
        s = rp["size"]
        p = rp["place"]
        t = time.time() - rp["spawntime"]
        v = rp["speed"]
        r = (c >> 16) & 0xFF
        g = (c >> 8) & 0xFF
        b = c & 0xFF

        def phase(x): return t * v - abs(x - p) - s

        def magni(x): return 1 - abs(math.sin(
            phase(x) * math.pi / 2 / s)) if abs(phase(x)) <= s else 0

        effect_row = [
            [int(magni(i) * x) for x in [r, g, b]]
            for i in range(num)
        ]

        for i in range(num):
            for j in range(3):
                rgb_row[i][j] = min(rgb_row[i][j] + effect_row[i][j], 255)

    for i in range(num):
        r, g, b = rgb_row[i]
        strip.setPixelColorRGB(i, r, g, b)
    strip.show()


def ripple_mode(strip,
                ripple_per_sec=1,
                ripple_cooldown=0.3,
                ripple_size=3.0,
                ripple_speed=8.0,
                fps=120):
    num = strip.numPixels()
    # ripple: {place, color, spawntime, size, speed, lifetime}
    ripples = []

    last_ripple_spawn_time = time.time() - ripple_cooldown

    while True:
        # spawn procedure
        if time.time() - last_ripple_spawn_time >= ripple_cooldown:
            spawn_rand = random.random()

            if spawn_rand <= ripple_per_sec / fps:
                place_rand = random.randint(0, num - 1)
                color_rand_float = colorsys.hsv_to_rgb(
                    random.random(), 1, 1
                )
                color_rand = [
                    min(int(x * 256), 255)
                    for x in color_rand_float
                ]

                rp_travel_length = abs(
                    place_rand - num / 2) + (num / 2) + ripple_size
                rp_lifetime = rp_travel_length / ripple_speed

                ripples.append({
                    "place": place_rand,
                    "color": Color(*color_rand),
                    "spawntime": time.time(),
                    "size": ripple_size,
                    "speed": ripple_speed,
                    "lifetime": rp_lifetime
                })

                last_ripple_spawn_time = time.time()

        # send light data
        light_ripples(strip, ripples)

        # prune old ripple
        ripples = [rp for rp in ripples if time.time() - rp["spawntime"]
                   < rp["lifetime"]]

        # wait for next tick
        time.sleep(1 / fps)


def single(strip, color):
    num = strip.numPixels()
    for i in range(num):
        strip.setPixelColor(i, color)
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

            ripple_mode(strip)

            time.sleep(WAIT_MS / 1000)

    except KeyboardInterrupt:
        blank(strip)
        del(strip)
        raise
