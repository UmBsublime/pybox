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
        trim_content = []
        for e in content:
            trim_content.append(e[:16])
        self.content = trim_content
        self.color = color
        pass

    def get_current_lines(self):
        pass

    def _rotate(self, direction=1):
        t = deque(self.content)
        t.rotate(direction)
        self.content = list(t)


class MenuType(BaseType):

    def __init__(self, menu, color):
        '''
            menu is a list of
            [('demo_file', reference_to_FileType),
             ('demo_menu', reference_to_MenuType),
             ('demo_dyn', reference_to_DynamicType),
             . . .]
        '''
        self.menu = menu
        content = []
        for i in menu:
            content.append(i[0])
        super(MenuType, self).__init__(content, color)

    def _rotate(self, direction=1):
        t = deque(self.menu)
        t.rotate(direction)
        self.menu = list(t)

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
                self._rotate(-1)
                lines = self.get_current_lines()
            if LCD.is_pressed(BUTTONS['Up']):
                self._rotate()
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

    def get_current_lines(self, pointer=' '):


        line1 = list(self.content)[0]
        line2 = list(self.content)[1]

        lines = [pointer+line1,
                 ' '+line2]
        return lines

    def execute(self, pointer=None):
        if pointer:
            lines = self.get_current_lines('\x05')
        else:
            lines = self.get_current_lines()
        #lines = self.get_current_lines()
        BaseType.plate.set_lines(lines[0], lines[1])
        BaseType.plate.update_plate(self.color)
        time.sleep(WHILE_DELAY*2)
        while True:
            if LCD.is_pressed(BUTTONS['Down']):
                self._rotate(-1)
                if pointer:
                    lines = self.get_current_lines('\x05')
                else:
                    lines = self.get_current_lines()
            if LCD.is_pressed(BUTTONS['Up']):
                self._rotate()
                if pointer:
                    lines = self.get_current_lines('\x05')
                else:
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


from lcdmpd import Py3status

class MpdListType(ScrollType):
    def __init__(self, color, right_action=None):

        self.right_action = right_action
        self.mpd = Py3status()
        content = self.mpd.artist_list()
        content = content.content
        content.append('dummy artist')
        print content
        super(ScrollType, self).__init__(content, color)

    def get_list(self, query = ''):
        if query == '':
            list = self.mpd.artist_list()
        else:
            list = self.mpd.song_list(query)

        return list

    def execute(self, pointer='\x05'):
        lines = self.get_current_lines('\x05')
        BaseType.plate.set_lines(lines[0], lines[1])
        BaseType.plate.update_plate(self.color)
        time.sleep(WHILE_DELAY*2)
        while True:
            if LCD.is_pressed(BUTTONS['Down']):
                self._rotate(-1)
                lines = self.get_current_lines('\x05')
            if LCD.is_pressed(BUTTONS['Up']):
                self._rotate()
                lines = self.get_current_lines('\x05')
            if LCD.is_pressed(BUTTONS['Left']):
                time.sleep(WHILE_DELAY*2)
                break
            if LCD.is_pressed(BUTTONS['Right']):
                t = self.get_list(self.content[0])
                time.sleep(WHILE_DELAY*2)
                t.execute(pointer)

            BaseType.plate.set_lines(lines[0], lines[1])
            ScrollType.plate.update_plate(self.color)
            time.sleep(WHILE_DELAY)

class LeafType():
    def __init__(self):
        pass

def main():
    def dummy():
        return ['dummy', 'reporting in']
    filet = ScrollType(['test file1', 'test file2', 'test file3'], GREEN)
    dyn = DynamicType(dummy, BLUE)
    menu = MenuType([('dyn', dyn),
                     ('filet', filet)], RED)

    print menu.__dict__
    print filet.__dict__
    print dyn.__dict__

    while True:
        menu.execute()


if __name__ == '__main__':
    main()
