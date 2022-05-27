import math
import random

def lerp(x, x0, x1, y0, y1):
    """
    Calculate linear interpolation. Clamp x within x0 and x1 bounds.
    """
    if x > x1:
        x = x1
    if x < x0:
        x = x0
    return round(y0 + (y1 - y0) * ((x - x0) / (x1 - x0)))

def lerp3(x, x0, x1, y0, y1):
    """
    Calculate linear interpolation of all values of 3-tuple.
    """
    return lerp(x, x0, x1, y0[0], y1[0]), lerp(x, x0, x1, y0[1], y1[1]), lerp(x, x0, x1, y0[2], y1[2])

def random_cycler(min, max):
    """
    Iterate from min up to a random number less than max, and then continue to do so up to a new
    random number each time
    """
    while True:
        random_max = random.randint(min, max)
        for i in range(random_max):
            yield i, random_max

def random_sin_cycler(min, max):
    """
    Spend randint(min, max) frames iterating over one cycle of a sin function
    """
    cycler = random_cycler(min, max)
    while True:
        cycle_x, cycle_max = next(cycler)
        yield math.sin(2 * math.pi * cycle_x / cycle_max)

def dim(pixel, percentage):
    """
    Dim a pixel by percentage, using lerp between black and color. percentage: 0 -> black, 1 -> color
    """
    def dim_color(color, percentage):
        return lerp(percentage, 0, 1, 0, color)
    return dim_color(pixel[0], percentage), dim_color(pixel[1], percentage), dim_color(pixel[2], percentage)
