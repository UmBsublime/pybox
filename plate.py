from variables import LCD


class Plate():

    def __init__(self):
        self.color = (0, 0, 0)
        self.lines = {1: '',
                      2: ''}
        self.old_lines = {1: '',
                          2: ''}

    def set_color(self, color):
        self.color = color

    def set_line(self, message, line=1):
        self.old_lines[line] = self.lines[line]
        self.lines[line] = message[:16]

    def set_lines(self, line_1='', line_2=''):
        self.old_lines[1] = self.lines[1]
        self.old_lines[2] = self.lines[2]

        self.lines[1] = line_1[:16]
        self.lines[2] = line_2[:16]

    def get_lines(self):
        return self.lines[1] + '\n' + self.lines[2]

    def update_plate(self, color=()):
        if self.lines != self.old_lines:
            LCD.clear()
            LCD.message(self.get_lines())
            if color is not ():
                LCD.set_color(*color)
            else:
                LCD.set_color(*self.color)
