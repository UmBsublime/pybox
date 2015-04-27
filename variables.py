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

COMMAND_DELAY = 0.8
WHILE_DELAY = 0.1

BUTTONS = {'Up': Adafruit_LCD.UP,
           'Down': Adafruit_LCD.DOWN,
           'Left': Adafruit_LCD.LEFT,
           'Right': Adafruit_LCD.RIGHT,
           'Select': Adafruit_LCD.SELECT}
