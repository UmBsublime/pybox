import Adafruit_CharLCD as Adafruit_LCD

LCD = Adafruit_LCD.Adafruit_CharLCDPlate()
WHITE = (1, 1, 1)
MAGENTA = (1, 0, 1)
CYAN = (0, 1, 1)
YELLOW = (1, 1, 0)
BLUE = (0, 0, 1)
GREEN = (0, 1, 0)
RED = (1, 0, 0)
OFF = (0, 0, 0)

# create some custom characters
# Music Note
LCD.create_char(1, [2, 3, 2, 2, 14, 30, 12, 0])
#SPEAKER
LCD.create_char(2, [1, 2, 15, 15, 15, 3, 1, 0])

# Clock
LCD.create_char(3, [0, 14, 21, 23, 17, 14, 0, 0])

# Stop / Square
LCD.create_char(4, [31, 17, 10, 4, 10, 17, 31, 0])
# Play / Right Arrow
LCD.create_char(5, [8, 12, 10, 9, 10, 12, 8, 0])
# Left Arrow
LCD.create_char(6, [2, 6, 10, 18, 10, 6, 2, 0])


#WTF
#LCD.create_char(7, [31, 17, 21, 21, 21, 21, 17, 31])
# Check Mark
#LCD.create_char(2, [0, 1, 3, 22, 28, 8, 0, 0])

COMMAND_DELAY = 3.0
WHILE_DELAY = 0.1

BUTTONS = {'Up': Adafruit_LCD.UP,
           'Down': Adafruit_LCD.DOWN,
           'Left': Adafruit_LCD.LEFT,
           'Right': Adafruit_LCD.RIGHT,
           'Select': Adafruit_LCD.SELECT}
