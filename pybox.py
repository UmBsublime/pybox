#!/usr/bin/env python

# MAIN

import time

import commands
from plate import Plate
from widget_types import ScrollType, DynamicType, MenuType
from variables import *


def main():

    ipconfig = ScrollType(commands.ipconfig(), GREEN)
    ls_root = ScrollType(commands.ls('/'), GREEN)
    df = ScrollType(commands.df(), GREEN)
    who = ScrollType(commands.who(), GREEN)
    pybox_help = ScrollType(commands.pybox_help(), GREEN)

    mem_info = DynamicType(commands.mem_info, CYAN)
    run_time = DynamicType(commands.runtime, BLUE, 0.75)
    uptime = DynamicType(commands.uptime, CYAN)
    hostname = DynamicType(commands.hostname, YELLOW)

    status = MenuType([('Hostname', hostname),
                       ('Uptime', uptime),
                       ('Who', who),
                       ('Ip Config', ipconfig),
                       ('Disk Usage', df),
                       ('Mem Info', mem_info)], WHITE)

    menu = MenuType([('Help', pybox_help),
                     ('Runtime', run_time),
                     ('ls /', ls_root),
                     ('Status', status)], WHITE)
    from pprint import pprint
    for i in list(menu.__dict__['menu']):
        print
        pprint(i[1].__dict__,indent=4)

    menu.execute()

    line1 = '{:^16}'.format('Quit ?')
    line2 = '{:^16}'.format('Yes\x06 \x05No')
    while True:
        plate.set_lines(line1, line2)
        plate.update_plate(RED)
        if LCD.is_pressed(BUTTONS['Left']):
            break
        elif LCD.is_pressed(BUTTONS['Right']):
            time.sleep(WHILE_DELAY*2)
            menu.execute()
        time.sleep(WHILE_DELAY)

if __name__ == '__main__':

    plate = Plate()

    print 'Press Ctrl-C to quit.'
    try:
        main()
    except KeyboardInterrupt:
        pass
    plate.set_lines('{:^16}'.format('Goodbye'), '')
    plate.update_plate(WHITE)
    time.sleep(0.3)
    plate.set_lines('', '')
    plate.update_plate(OFF)
