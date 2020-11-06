#!/usr/bin/env python3

import os, sched, time
from waveshare_epd import epd2in13_V2
from inky import InkyPHAT_SSD1608
from PIL import Image,ImageDraw,ImageFont

curdir = os.path.dirname(os.path.realpath(__file__))
gfxdir = os.path.join(curdir, 'gfx')

scheduler = sched.scheduler(time.time, time.sleep)

try:
    # setup clock screen
    clock_epd = epd2in13_V2.EPD()

    # resources for clock screen
    font_numbers = [ Image.open(os.path.join(gfxdir, '0.bmp')),
            Image.open(os.path.join(gfxdir, '1.bmp')),
            Image.open(os.path.join(gfxdir, '2.bmp')),
            Image.open(os.path.join(gfxdir, '3.bmp')),
            Image.open(os.path.join(gfxdir, '4.bmp')),
            Image.open(os.path.join(gfxdir, '5.bmp')),
            Image.open(os.path.join(gfxdir, '6.bmp')),
            Image.open(os.path.join(gfxdir, '7.bmp')),
            Image.open(os.path.join(gfxdir, '8.bmp')),
            Image.open(os.path.join(gfxdir, '9.bmp'))
        ]
    font_separator = Image.open(os.path.join(gfxdir, 'separator.bmp'))

    time_image = Image.new('1', (clock_epd.height, clock_epd.width), 255)
    time_draw = ImageDraw.Draw(time_image)

    # setup calendar screen


except IOError as e:
    print(e)
    exit(2)

def print_time(time, msg = ''):
    print('{}{:02d}:{:02d}:{:02d}'.format(
            msg, time.tm_hour, time.tm_min, time.tm_sec))

def get_next_update_epoch():
    cur_time_epoch = time.time()
    cur_time = time.localtime(cur_time_epoch)
    next_update_at_epoch = cur_time_epoch + 60 - cur_time.tm_sec
    return next_update_at_epoch

def update_display(refresh = False):
    # do thing here
    cur_time = time.localtime()
    print_time(cur_time, 'updating at: ')

    time_draw.rectangle((0, 0, 250, 122), fill = 255)
    time_image.paste(font_numbers[int(cur_time.tm_hour // 10)], (13, 20))
    time_image.paste(font_numbers[int(cur_time.tm_hour % 10)], (61, 20))
    time_image.paste(font_separator, (109, 20))
    time_image.paste(font_numbers[int(cur_time.tm_min // 10)], (141, 20))
    time_image.paste(font_numbers[int(cur_time.tm_min % 10)], (189, 20))

    if refresh:
        clock_epd.init(clock_epd.FULL_UPDATE)
        clock_epd.displayPartBaseImage(clock_epd.getbuffer(time_image.rotate(180)))
    else:
        clock_epd.init(clock_epd.PART_UPDATE)
        clock_epd.displayPartial(clock_epd.getbuffer(time_image.rotate(180)))
    clock_epd.sleep()

    # schedule the next update, refresh the screen if the hour is gonna change
    print_time(time.localtime(), 'updated at: ')
    next_update_at_epoch = get_next_update_epoch()
    print_time(time.localtime(next_update_at_epoch), 'next update at: ')
    refresh = cur_time.tm_hour != time.localtime(next_update_at_epoch).tm_hour
    scheduler.enterabs(next_update_at_epoch, 1, update_display, argument=(refresh,))

# schedule the first update immediately and start the scheduler running
scheduler.enter(0, 1, update_display, argument=(True,))
try:
    scheduler.run()
except KeyboardInterrupt:
    print('keyboard interrupt, quitting')
    exit()
