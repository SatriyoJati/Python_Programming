import board
import busio
import RPi.GPIO as GPIO
import time
from adafruit_mcp230xx.mcp23017 import MCP23017


pin_relay_atas = 25

def init_relay_atas(value):
    if value :
        GPIO.setwarnings(False)
        #setup GPIOs
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin_relay_atas, GPIO.OUT)
        time.sleep(2)
        #set HIGH main board
        GPIO.output(pin_relay_atas, GPIO.HIGH)
    else :
        GPIO.setwarnings(False)
        #setup GPIOs
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin_relay_atas, GPIO.OUT)
        time.sleep(2)
        #set HIGH main board
        GPIO.output(pin_relay_atas, GPIO.LOW)

    return True


if "__main__" == __name__ :
    try:
        ret = init_relay_atas(True)
        if ret:
            delay = 20
            print("delay for {}".format(delay))
            i2c = busio.I2C(board.SCL, board.SDA)
            time.sleep(delay)
            mcp = MCP23017(i2c, address = 0x27)
        test = input("Press enter to stop program ").lower()

    except OSError as e :
        print(type(e))
        print("Remote I/O Error")

    except KeyboardInterrupt as e:
        print(type(e))
        print("KeyboardInterupt")

    except Exception as e:
        print(e)
        #init_relay_atas(False)

    else:
        if test == 'y':
            init_relay_atas(False)
