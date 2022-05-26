import board
import neopixel

class PixelConfig:
    # frames per second
    fps = 30

    # total number of LEDs
    count = 50

    def __init__(self) -> None:
        self.pixels = neopixel.NeoPixel(
            board.GP0,
            self.count,
            auto_write=False,
            brightness=0.3,
            pixel_order=neopixel.GRB
        )
