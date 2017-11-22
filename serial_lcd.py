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

	def createCustomChar(self, address, pattern):
		#set cgrom address
		LOG.debug("Creating custom character in CGROM")
		customCharPattern = bytearray.fromhex(pattern)
		cgromInstr = bytearray.fromhex(u'FE')
		cgromInstr.append(64+(address)) #0x40 + 1...8
		ser.write(cgromInstr) #Send cgrom command to LCD
		LOG.debug("Writing Pattern to %d", cgromInstr[1])
		for element in customCharPattern:
			ser.write(bytearray([element]))

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

	LOG.info('Configuring /dev/serial0 dialout 96001N8')
	ser = serial.Serial(
		port='/dev/serial0',
		baudrate = 9600,
		parity=serial.PARITY_NONE,
		stopbits=serial.STOPBITS_ONE,
		bytesize=serial.EIGHTBITS,
		timeout=1
		)

	try:
		ser.isOpen()
		LOG.info('/dev/serial0 dialout ready for action')

	except IOError as ioe:
		ser.close()
		ser.open()
		LOG.info("/dev/serial0 was already open, was closed and opened again!")

	time.sleep(0.5)		#display init delay

	display = LcdDisplay('', '', 0, 0)
	display.initializeLcd()
	display.setCursorPosition(0, 4)
	display.setDisplayText('WiZard')

	#set cgrom address
	pacman_0 = bytearray.fromhex("00 00 00 01 07 0F 0F 1F")
	cgramChar0Base =  64 #  0x40
	counter = 0
	for element in pacman_0:
		ser.write(bytearray.fromhex(u'FE'))
		cgramAddress = cgramChar0Base + counter
		ser.write(bytearray([cgramAddress]))
		time.sleep(0.0005)
		ser.write(bytearray([element]))
		counter += 1

	display.setCursorPosition(0, 0)
	ser.write(bytearray.fromhex(u'00')) #CGROM address 0 = custom char 0

	#set cgrom address
	pacman_1 = bytearray.fromhex("00 00 00 10 1c 0e 1e 1f")
	cgramChar1Base =  72 #  0x48
	counter = 0
	for element in pacman_1:
		ser.write(bytearray.fromhex(u'FE'))
		cgramAddress = cgramChar1Base + counter
		ser.write(bytearray([cgramAddress]))
		time.sleep(0.0005)
		ser.write(bytearray([element]))
		counter += 1

	display.setCursorPosition(0, 1)
	ser.write(bytearray.fromhex(u'01')) #CGROM address 1 = custom char 1

	#set cgrom address
	pacman_2 = bytearray.fromhex("1f 0f 0f 07 01 00 00 00")
	cgramChar2Base =  80 #  0x50
	counter = 0
	for element in pacman_2:
		ser.write(bytearray.fromhex(u'FE'))
		cgramAddress = cgramChar2Base + counter
		ser.write(bytearray([cgramAddress]))
		time.sleep(0.0005)
		ser.write(bytearray([element]))
		counter += 1

	display.setCursorPosition(1, 0)
	ser.write(bytearray.fromhex(u'02')) #CGROM address 2 = custom char 2

	#set cgrom address
	pacman_3 = bytearray.fromhex("1f 1e 1e 1c 10 00 00 00")
	cgramChar3Base =  88 #  0x58
	counter = 0
	for element in pacman_3:
		ser.write(bytearray.fromhex(u'FE'))
		cgramAddress = cgramChar3Base + counter
		ser.write(bytearray([cgramAddress]))
		time.sleep(0.0005)
		ser.write(bytearray([element]))
		counter += 1

	display.setCursorPosition(1, 1)
	ser.write(bytearray.fromhex(u'03')) #CGROM address 3 = custom char 3

	display.setCursorPosition(0, 14)
	ser.write(bytearray.fromhex(u'00')) #PACMAN Back TOP

	display.setCursorPosition(1, 14)
	ser.write(bytearray.fromhex(u'02')) #PACMAN Back BOTTOM

	#set cgrom address
	pacman_4 = bytearray.fromhex("00 00 00 10 1c 0e 1c 10")
	cgramChar4Base =  96 #  0x60
	counter = 0
	for element in pacman_4:
		ser.write(bytearray.fromhex(u'FE'))
		cgramAddress = cgramChar4Base + counter
		ser.write(bytearray([cgramAddress]))
		time.sleep(0.0005)
		ser.write(bytearray([element]))
		counter += 1

	display.setCursorPosition(0, 15)
	ser.write(bytearray.fromhex(u'04')) #CGROM address 4 = custom char 4

	#set cgrom address
	pacman_5 = bytearray.fromhex("10 1c 1e 1c 10 00 00 00")
	cgramChar5Base =  104 #  0x68
	counter = 0
	for element in pacman_5:
		ser.write(bytearray.fromhex(u'FE'))
		cgramAddress = cgramChar5Base + counter
		ser.write(bytearray([cgramAddress]))
		time.sleep(0.0005)
		ser.write(bytearray([element]))
		counter += 1

	display.setCursorPosition(1, 15)
	ser.write(bytearray.fromhex(u'05')) #CGROM address 5 = custom char 5


	while True:
		pass