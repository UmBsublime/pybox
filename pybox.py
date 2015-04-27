#!/usr/bin/env python

# MAIN

import time

import commands
from plate import Plate
from wheel import WheelMenu
from variables import *
from collections import deque
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

    settings = deque([('Ip config', commands.ipconfig),
                      ('Uptime/Load', commands.uptime)])

    status = deque([('Ip config', commands.ipconfig),
                    ('Uptime/Load', commands.uptime),
                    ('hostname', commands.hostname),
                    ('MemInfo', commands.mem_info)])

    dir = deque([('ls', commands.ls),
                 ('Placeholder', commands.ls)])
    plate.set_color(WHITE)
    menu = WheelMenu(plate, [('Settings', settings),
                             ('Status', status),
                             ('Dir', dir)])


    menu.do_loop()
    line1 = '{:^16}'.format('Quit ?')
    line2 = '{:^16}'.format('Yes\x06 \x05No')

    while True:
        plate.set_lines(line1, line2)
        plate.update_plate(RED)
        if LCD.is_pressed(BUTTONS['Left']):
            plate.set_lines('{:^16}'.format('Goodbye'), '')
            plate.update_plate(WHITE)
            time.sleep(2)
            plate.set_lines('', '')
            plate.update_plate(OFF)
            break
        elif LCD.is_pressed(BUTTONS['Right']):
            time.sleep(WHILE_DELAY*2)
            menu.do_loop()
        time.sleep(WHILE_DELAY)



if __name__ == '__main__':
    main()
