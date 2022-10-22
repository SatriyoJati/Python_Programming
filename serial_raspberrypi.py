#!/usr/bin/env python

import serial

test_string = "Test serial port ...".encode('utf-8')
#UART0 --> serial0 --> /dev/ttyAMA0 for bluetooth
port = "/dev/ttyS0" #Connected to UART1,
baud_rate = 9600

ser = serial.Serial(
    port= port,
    baudrate= baud_rate,
    parity = serial.PARITY_NONE,
    stopbits = serial.STOPBITS_ONE,
    bytesize = serial.EIGHTBITS,
    timeout = 1
)

while True:
    rx_data = ser.readlines()
    print(rx_data)
    time.sleep(1)
