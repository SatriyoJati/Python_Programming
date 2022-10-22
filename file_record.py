import os
import subprocess


def appendFile(self, msg):
    heading = datetime.now().strftime("--%H:%M:%S--")
    data = "{} {} -> {}\n".format(heading, datetime.now().strftime("%d %B %Y"), msg)
    file = './log_pm2.txt'
    hs = open(file,"a")
    hs.write(data)
    hs.close()
