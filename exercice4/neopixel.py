# neopixel.py - pilote pour WS2812 / WS2813 (NeoPixel)
import array, time
from machine import Pin

class NeoPixel:
    ORDER = (1, 0, 2, 3)
    def __init__(self, pin, n, bpp=3, timing=0):
        self.pin = pin
        self.n = n
        self.bpp = bpp
        self.buf = array.array("I", [0 for _ in range(n)])
        self.pin.init(Pin.OUT)

    def __setitem__(self, index, val):
        if not (0 <= index < self.n):
            raise IndexError
        r, g, b = val
        self.buf[index] = (g << 16) | (r << 8) | b

    def __getitem__(self, index):
        if not (0 <= index < self.n):
            raise IndexError
        v = self.buf[index]
        return ((v >> 8) & 0xff, (v >> 16) & 0xff, v & 0xff)

    def fill(self, color):
        for i in range(self.n):
            self[i] = color

    def write(self):
        import neopixel_write
        neopixel_write.neopixel_write(self.pin, self.buf, True)
