#Logger Kios

import subprocess
import re
import os
import datetime

file1 = "/home/pi/pameran_log_file_embedded.txt"
file2 = "/home/pi/pameran_log_file_sendToBe.txt"
file3 = "/home/pi/pameran_log_file_subreqres.txt"
file4 = "/home/pi/pameran_log_file_main_server.txt"

with open(file1, 'w') as f1, open(file2, 'w') as f2, open(file3, 'w') as f3, open(file4, 'w') as f4:
    subprocess.Popen(["sudo", "pm2" , "logs", "0"],stdout=f1)
    subprocess.Popen(["sudo", "pm2" , "logs", "2"],stdout=f2)
    subprocess.Popen(["pm2" , "logs", "1"],stdout=f3)
    subprocess.Popen(["sudo", "pm2" , "logs", "1"],stdout=f4)

# with open(file1, 'w') as f1, open(file2, 'w') as f2, open(file3, 'w') as f3, open(file4, 'w') as f4:
#     subprocess.call(["sudo", "pm2" , "logs", "0", ">>", "/home/pi/pameran_log_file_embedded.txt" ],stdout=f1)
#     subprocess.call(["sudo", "pm2" , "logs", "2", ">>", "/home/pi/pameran_log_file_sendToBe.txt"],stdout=f2)
#     subprocess.call(["pm2" , "logs", "1", ">>", "/home/pi/pameran_log_file_subreqres.txt"],stdout=f3)
#     subprocess.call(["sudo", "pm2" , "logs", "1", ">>", "/home/pi/pameran_log_file_main_server.txt"],stdout=f4)


# os.system('sudo pm2 logs 2 >> /home/pi/pameran_log_file_sendToBe.txt')
# os.system('pm2 logs 1 >> /home/pi/pameran_log_file_subreqres.txt')
# os.system('sudo pm2 logs 1>> /home/pi/pameran_log_file_main_server.txt')
