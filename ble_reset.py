#BLE restart via systemd

import os
import re
import subprocess

while True :
    if re.findall('DOWN INIT RUNNING', subprocess.getoutput('hciconfig')):
        os.system("sudo /etc/init.d/bluetooth restart")
        time.sleep(1)

    if re.findall('DOWN', subprocess.getoutput('hciconfig')):
        os.system("sudo hciconfig hci0 up")
        time.sleep(1)

    if re.findall('UP RUNNING', subprocess.getoutput('hciconfig')):
        break
