import time

from collections import deque
from variables import *


class WheelMenu():

    def __init__(self, plate, menu):
        self.plate = plate
        self.menu = deque(menu)
        self.menu_size = 2

    def print_menu(self):
        line1 = list(self.menu)[0][0]
        line2 = list(self.menu)[1][0]
        self.plate.set_lines('\x05'+line1, ' '+line2)
        self.plate.update_plate()

    def rotate(self, direction=1):
        self.menu.rotate(direction)

    def do_command(self):
        command = list(self.menu)[0][1]
        #result = command()

        if isinstance(command, deque):
            print 'deque'
            old_menu = self.menu
            self.menu = command
            while self.do_loop():
                pass
            self.menu = old_menu

        # For now if a list is returned let's asume WheelText
        elif isinstance(command(), list):
            result = command()
            old_color = self.plate.color
            wheel = WheelText(self.plate, result, GREEN)
            wheel.do_loop()
            self.plate.set_color(old_color)


        # Else asume result is a tuple (line1, line2)
        else:
            lines = command()
            counter = 0
            while not LCD.is_pressed(BUTTONS['Left']):
                if counter >= COMMAND_DELAY:
                    lines = command()
                    counter = 0
                counter += WHILE_DELAY

                self.plate.set_lines(lines[0], lines[1])
                self.plate.update_plate(CYAN)
                time.sleep(WHILE_DELAY)

    def do_loop(self):
        self.print_menu()
        while True:
            self.print_menu()
            if LCD.is_pressed(BUTTONS['Down']):
                self.rotate(-1)
            if LCD.is_pressed(BUTTONS['Up']):
                self.rotate()
            if LCD.is_pressed(BUTTONS['Right']):
                self.do_command()
            if LCD.is_pressed(BUTTONS['Left']):
                time.sleep(WHILE_DELAY*2)
                break
            self.print_menu()
            time.sleep(WHILE_DELAY)

class WheelText():

    def __init__(self, plate, text, color=()):
        self.plate = plate
        self.text = deque(text)
        self.menu_size = 2
        self.color = color

    def rotate(self, direction=1):
        self.text.rotate(direction)

    def print_text(self):
        line1 = list(self.text)[0]
        line2 = list(self.text)[1]
        self.plate.set_color(self.color)
        self.plate.set_lines('\x05'+str(line1), ' '+str(line2))
        self.plate.update_plate()

    def do_loop(self):
        self.print_text()
        while True:
            if LCD.is_pressed(BUTTONS['Down']):
                self.rotate(-1)
            if LCD.is_pressed(BUTTONS['Up']):
                self.rotate()
            if LCD.is_pressed(BUTTONS['Left']):
                time.sleep(WHILE_DELAY*2)
                break
            self.print_text()
            time.sleep(WHILE_DELAY)