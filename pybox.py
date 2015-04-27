#!/usr/bin/env python

# MAIN

import time

import commands
from plate import Plate
from wheel import WheelMenu
from variables import *

# create some custom characters
LCD.create_char(1, [2, 3, 2, 2, 14, 30, 12, 0])
LCD.create_char(2, [0, 1, 3, 22, 28, 8, 0, 0])
LCD.create_char(3, [0, 14, 21, 23, 17, 14, 0, 0])
LCD.create_char(4, [31, 17, 10, 4, 10, 17, 31, 0])
LCD.create_char(5, [8, 12, 10, 9, 10, 12, 8, 0])
LCD.create_char(6, [2, 6, 10, 18, 10, 6, 2, 0])
LCD.create_char(7, [31, 17, 21, 21, 21, 21, 17, 31])


def main():
    print 'Press Ctrl-C to quit.'
    plate = Plate()

    menu = WheelMenu(plate, [('Ip config', commands.ipconfig),
                             ('Uptime/Load', commands.uptime),
                             ('hostname', commands.hostname),
                             ('MemInfo', commands.mem_info),
                             ('ls', commands.ls)])
    plate.set_color(WHITE)
    settings = WheelMenu(plate, [('Settings', menu),
                                 ('Blank', 'blank')])
    '''
    while True:
        settings.print_menu()
        if LCD.is_pressed(BUTTONS['Down']):
            settings.rotate(-1)
        if LCD.is_pressed(BUTTONS['Up']):
            settings.rotate()
        if LCD.is_pressed(BUTTONS['Right']):
            settings.do_command()

        time.sleep(WHILE_DELAY)
    '''
    while True:
        menu.print_menu()
        if LCD.is_pressed(BUTTONS['Down']):
            menu.rotate(-1)
        if LCD.is_pressed(BUTTONS['Up']):
            menu.rotate()
        if LCD.is_pressed(BUTTONS['Right']):
            menu.do_command()
        time.sleep(WHILE_DELAY)


if __name__ == '__main__':
    main()
