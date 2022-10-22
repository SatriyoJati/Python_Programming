import board
import busio
i2c = busio.I2C(board.SCL, board.SDA)

import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

ads = ADS.ADS1015(i2c)
chan = AnalogIn(ads, ADS.P2)
while(1):
    print('value:', chan.value)
    data = chan.value 
    if  data > 9000:
        print("{}   detected, value: {}".format(count,data))
        count+=1
        time.sleep(1)
