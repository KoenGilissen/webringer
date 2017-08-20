#!/usr/bin/env python
__author__ = "Dr. Ing. Koen Gilissen"
__version__ = "1.0.0"
__maintainer__ = "Dr. Ing. Koen Gilissen"
__email__ = "gilissenkoen@gmail.com"

import serial
import time
import lcdConstants

ser = serial.Serial(
	#port='/dev/ttyAMA0',
	port='/dev/serial0',
    baudrate = 9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
   	bytesize=serial.EIGHTBITS,
    timeout=1
    )

time.sleep(1)		#display init delay

#s = bytearray.fromhex(u'FE 01 FE 0F FE 80')

ser.write(lcdConstants.clearDisplay)
ser.write(lcdConstants.turnOnDisplayCursorBlinking)
ser.write(lcdConstants.cursorHomeLine0)
ser.write('Embedded Linux')
ser.write(lcdConstants.cursorHomeLine1)
ser.write('Wizard')
while True:
	pass