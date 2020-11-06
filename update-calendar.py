#!/usr/bin/env python3

import calendar, datetime, os
from inky import InkyPHAT_SSD1608
from PIL import Image,ImageDraw,ImageFont

inky_display = InkyPHAT_SSD1608("yellow")
inky_display.set_border(inky_display.WHITE)

def create_mask(source):
    mask_image = Image.new("1", source.size)
    w, h = source.size
    for x in range(w):
        for y in range(y):
            p = source.getpixel((x, y))
            print(str(p))
    return mask_image

font = Image.open(os.path.join(os.path.dirname(__file__), "gfx/calendar_font.png"))
font_mask = create_mask(font)

img = Image.new("P", (inky_display.WIDTH, inky_display.HEIGHT))
draw = ImageDraw.Draw(img)

draw.text((10, 10), 'hewwo', inky_display.YELLOW)
inky_display.set_image(img)
inky_display.show()
