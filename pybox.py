#!/usr/bin/env python

# MAIN

import time

import commands
from widget_types import ScrollType, DynamicType, MenuType
from variables import *


def main():

    print 'Press Ctrl-C to quit.'

    from plate import Plate
    plate = Plate()
    ipconf = ScrollType(commands.ipconfig(),GREEN)
    ls_root = ScrollType(commands.ls('/'),GREEN)
    run_time = DynamicType(commands.runtime, BLUE, 0.75)

    uptime = DynamicType(commands.uptime, CYAN)
    hostname = DynamicType(commands.hostname,YELLOW)

    menu = MenuType([('Runtime',run_time),
                     ('ls /',ls_root),
                     ('Ip Config', ipconf),
                     ('Uptime', uptime),
                     ('Hostname', hostname)], WHITE)

    menu.execute()

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
            menu.execute()
        time.sleep(WHILE_DELAY)

if __name__ == '__main__':
    main()
