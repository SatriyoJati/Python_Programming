#glucosemeter refactoring

import board
import busio
import time


i2c = busio.I2C(board.SCL, board.SDA)

def check_sound_adc():
    while time.
