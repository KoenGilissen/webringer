#!/usr/bin/env python
__author__ = "Dr. Ing. Koen Gilissen"
__version__ = "1.0.0"
__maintainer__ = "Dr. Ing. Koen Gilissen"
__email__ = "gilissenkoen@gmail.com"

import serial
import time
import lcdConstants
import logging
import argparse
from sys import stdout

# configure default logging
LOG = logging.getLogger('Serial LCD Driver')
FORMATTER = logging.Formatter(
	fmt='%(name) 12s|%(levelname) 6s|%(asctime) 20s|%(message)s',
	datefmt='%Y-%m-%d %H:%M:%S')
_SH = logging.StreamHandler(stdout)
_SH.setLevel(logging.DEBUG)
_SH.setFormatter(FORMATTER)
LOG.addHandler(_SH)


class LcdDisplay(object):
    """ LcdDisplay Class representing the LCD display 
    """
    def __init__(self, textLine0, textLine1, cursorX, cursorY):
        """ __init__ method for a LcdDisplay 

        Args:
            textLine0 (string): text on line 0 of the display DDram address 0x00 - 0x0F
            textLine1 (string): text on line 1 of the display DDram address 0xC0 - 0xCF
            cursorX (int): x coordinate of the cursor
            cursorY (int): y coordinate of the cursor
        """
        self.textLine0 = textLine0
        self.textLine1 = textLine1
        self.cursorX = cursorX
        self.cursorY = cursorY

    def initializeLcd(self):
    	LOG.info("Initializing LCD display")
    	ser.write(lcdConstants.clearDisplay)
    	ser.write(lcdConstants.turnOnDisplayCursorBlinking)
    	ser.write(lcdConstants.cursorHomeLine0)

    def setDisplayText(self, text):
    	LOG.debug("Setting display text %s", text)
    	ser.write(text)

    def setCursorPosition(self, line, position): #line <=1 position <= 15
    	ddramAdress = 0
    	if(position <= 15):
    		self.cursorX = position
    	else:
    		self.cursorX = 0
    	if(line == 1):
    		self.cursorY = 1
    		ddramAdress = 192
    	else:
    		self.cursorY = 0
    		ddramAdress = 128

    	LOG.debug("Setting cursor at line: %d at postion: %d", self.cursorY, self.cursorX)	
    	displayAddress = ddramAdress + self.cursorX
    	instruction = bytearray.fromhex(u'FE')
    	instruction.append(displayAddress)
    	ser.write(instruction)

    def __str__(self):
        """ Informal string representation of the LcdDisplay object.
        Returns:
            Formatted string containing the text diplayed and cursor position
        """
        return 'LcdDisplay \n{}\n{}\ncursor position: ({},{})'.format(self.textLine0, self.textLine1, self.cursorX, self.cursorY)

    def __repr__(self):
        """ official string representation of the LcdDisplay object.
        Returns:
            Formatted string containing the text diplayed and cursor position
        """
        return self.__str__()

if __name__ == '__main__':
	# 1) configure an argument parser
	parser = argparse.ArgumentParser(description='Serial LCD driver')
	#parser.add_argument('file', type=argparse.FileType('r'), help='Input file')
	parser.add_argument('-d', action='store_true', help='Turn on DEBUG output')
	parser.add_argument('-v', action='store_true', help='Turn on INFO output')

	args = parser.parse_args()

	# configure the log level dynamically
	LOG.setLevel(logging.WARN)
	if args.v:
		LOG.setLevel(logging.INFO)
	if args.d:
		LOG.setLevel(logging.DEBUG)

	try:
		LOG.info('Configuring /dev/serial0 dialout 96001N8')
		ser = serial.Serial(
			port='/dev/serial0',
			baudrate = 9600,
			parity=serial.PARITY_NONE,
			stopbits=serial.STOPBITS_ONE,
			bytesize=serial.EIGHTBITS,
			timeout=1
			)
		ser.isOpen()
		LOG.info('/dev/serial0 dialout ready for action')

	except IOError as ioe:
		ser.close()
		ser.open()
		LOG.info("/dev/serial0 was already open, was closed and opened again!")

	time.sleep(0.5)		#display init delay

	display = LcdDisplay('', '', 0, 0)
	display.initializeLcd()
	display.setCursorPosition(1, 5)
	display.setDisplayText('Python')
	display.setCursorPosition(0, 3)
	display.setDisplayText('WiZard')

	display.setCursorPosition(0, 0)
	for i in range(0, 16):
		#char = bytearray.fromhex(u'72')
		char = bytearray([i+161])
		ser.write(char)

	display.setCursorPosition(1, 0)
	for i in range(16, 32):
		#char = bytearray.fromhex(u'73')
		char = bytearray([i+161])
		ser.write(char)

	#set cgrom address
	customChar0 = bytearray.fromhex("00 0E 15 17 11 0E 00 00")
	cgromInstr0 = bytearray.fromhex(u'FE 40')
	

	ser.write(cgromInstr0)
	for element in customChar0:
		LOG.debug("element %d", element)
		ser.write(bytearray([element]))

	ser.write(lcdConstants.clearDisplay)
	ser.write(lcdConstants.cursorHomeLine0)
	cgomAddress = bytearray([0])
	ser.write(cgomAddress) 


	while True:
		pass