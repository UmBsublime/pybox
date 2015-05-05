import time

from collections import deque
from variables import *
from plate import Plate

class BaseType(object):

    plate = Plate()

    def __init__(self, content, color):
        '''
            content has to be a list of strings,
            if the strings are not 16 digit long,
            init will truncate
        '''
        self.content = deque(content)
        self.color = color
        pass

    def get_current_lines(self):
        pass

    def rotate(self, direction=1):
        self.content.rotate(direction)


class MenuType(BaseType):

    def __init__(self, menu, color):
        '''
            menu is a list of
            [('demo_file', reference_to_FileType),
             ('demo_menu', reference_to_MenuType),
             ('demo_dyn', reference_to_DynamicType),
             . . .]
        '''
        self.menu = deque(menu)
        content = []
        for i in menu:
            content.append(i[0])
        super(MenuType, self).__init__(content, color)

    def get_current_lines(self, pointer='\x05'):
        line1 = list(self.menu)[0][0]
        line2 = list(self.menu)[1][0]

        lines = [pointer+line1,
                 ' '+line2]
        return lines

    def execute(self):
        lines = self.get_current_lines()
        MenuType.plate.set_lines(lines[0], lines[1])
        MenuType.plate.update_plate(self.color)
        time.sleep(WHILE_DELAY*2)
        while True:
            if LCD.is_pressed(BUTTONS['Down']):
                self.menu.rotate(-1)
                lines = self.get_current_lines()
            if LCD.is_pressed(BUTTONS['Up']):
                self.menu.rotate()
                lines = self.get_current_lines()
            if LCD.is_pressed(BUTTONS['Left']):
                time.sleep(WHILE_DELAY*2)
                break
            if LCD.is_pressed(BUTTONS['Right']):
                time.sleep(WHILE_DELAY*2)
                list(self.menu)[0][1].execute()
            BaseType.plate.set_lines(lines[0], lines[1])
            BaseType.plate.update_plate(self.color)
            time.sleep(WHILE_DELAY)


class ScrollType(BaseType):

    def __init__(self, content, color):
        super(ScrollType, self).__init__(content, color)

    def get_current_lines(self):
        line1 = list(self.content)[0]
        line2 = list(self.content)[1]

        lines = [line1, line2]
        return lines

    def execute(self):
        lines = self.get_current_lines()
        BaseType.plate.set_lines(lines[0], lines[1])
        BaseType.plate.update_plate(self.color)
        time.sleep(WHILE_DELAY*2)
        while True:
            if LCD.is_pressed(BUTTONS['Down']):
                self.content.rotate(-1)
                lines = self.get_current_lines()
            if LCD.is_pressed(BUTTONS['Up']):
                self.content.rotate()
                lines = self.get_current_lines()
            if LCD.is_pressed(BUTTONS['Left']):
                time.sleep(WHILE_DELAY*2)
                break
            BaseType.plate.set_lines(lines[0], lines[1])
            ScrollType.plate.update_plate(self.color)
            time.sleep(WHILE_DELAY)


class DynamicType():

    plate = Plate()

    def __init__(self, function, color, delay=3.0):
        '''
            function, well, has to be a function...
        '''
        self.function = function
        self.color = color
        self.delay = delay
        #super(DynamicType, self).__init__(content)

    def get_current_lines(self):
        lines = self.function()
        return lines

    def execute(self):
        lines = self.get_current_lines()
        BaseType.plate.set_lines(lines[0], lines[1])
        BaseType.plate.update_plate(self.color)
        time.sleep(WHILE_DELAY)
        count = WHILE_DELAY
        while True:
            if LCD.is_pressed(BUTTONS['Left']):
                time.sleep(WHILE_DELAY*2)
                break

            if count >= self.delay:
                lines = self.get_current_lines()
                BaseType.plate.set_lines(lines[0], lines[1])
                count = 0

                BaseType.plate.update_plate(self.color)
            else:

                count += WHILE_DELAY
                time.sleep(WHILE_DELAY)


def main():
    def dummy():
        return ['dummy','reporting in']
    filet = ScrollType(['test file1', 'test file2', 'test file3'], GREEN)
    dyn = DynamicType(dummy, BLUE)
    menu = MenuType([('dyn',dyn),
                     ('filet',filet)], RED)


    print menu.__dict__
    print filet.__dict__
    print dyn.__dict__

    while True:
        menu.execute()

if __name__ == '__main__':
    main()

