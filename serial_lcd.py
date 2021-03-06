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
		ser.write(lcdConstants.turnOnDisplay)
		ser.write(lcdConstants.cursorHomeLine0)

		LcdDisplay.createCustomChar(self, lcdConstants.cgramChar0Base, lcdConstants.pacman0)
		LcdDisplay.createCustomChar(self, lcdConstants.cgramChar1Base, lcdConstants.pacman1)
		LcdDisplay.createCustomChar(self, lcdConstants.cgramChar2Base, lcdConstants.pacman2)
		LcdDisplay.createCustomChar(self, lcdConstants.cgramChar3Base, lcdConstants.pacman3)
		LcdDisplay.createCustomChar(self, lcdConstants.cgramChar4Base, lcdConstants.pacman4)
		LcdDisplay.createCustomChar(self, lcdConstants.cgramChar5Base, lcdConstants.pacman5)
		LcdDisplay.createCustomChar(self, lcdConstants.cgramChar6Base, lcdConstants.candyTop)
		LcdDisplay.createCustomChar(self, lcdConstants.cgramChar7Base, lcdConstants.candyBottom)

	def setDisplayText(self, text):
		LOG.debug("Setting display text %s", text)
		ser.write(text)

	def setCursorPosition(self, line, position): #line <=1 position <= lcdConstants.numberOfChars-1
		ddramAdress = 0
		if(position <= lcdConstants.numberOfChars-1):
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

	@staticmethod
	def createCustomChar(self, address, pattern):
		LOG.info("Creating Custom Char at: %d", address)
		cgramChar0Base =  address 
		counter = 0
		for element in pattern:
			ser.write(bytearray.fromhex(u'FE'))
			cgramAddress = cgramChar0Base + counter
			LOG.debug("address: %d element: %d", cgramAddress, element)
			ser.write(bytearray([cgramAddress]))
			time.sleep(0.0005)
			ser.write(bytearray([element]))
			counter += 1
		return 0

	def drawPacmanClosed(self, column):
		if(column < lcdConstants.numberOfChars-1):
			display.setCursorPosition(0, column) #PM back top
			ser.write(bytearray.fromhex(u'00')) 
			display.setCursorPosition(0, column+1)
			ser.write(bytearray.fromhex(u'01')) #PM closed front top
			display.setCursorPosition(1, column)
			ser.write(bytearray.fromhex(u'02')) #PM back bottom
			display.setCursorPosition(1, column+1)
			ser.write(bytearray.fromhex(u'03')) #PM closed front bottom

	def drawPacmanOpen(self, column):
		if(column < lcdConstants.numberOfChars-1):
			display.setCursorPosition(0, column) #PM back top
			ser.write(bytearray.fromhex(u'00')) 
			display.setCursorPosition(0, column+1)
			ser.write(bytearray.fromhex(u'04')) #PM open front top
			display.setCursorPosition(1, column)
			ser.write(bytearray.fromhex(u'02')) #PM  back bottom
			display.setCursorPosition(1, column+1)
			ser.write(bytearray.fromhex(u'05')) #PM open front bottom

	def drawCandy(self, column):
		if(column < lcdConstants.numberOfChars):
			display.setCursorPosition(0, column) #candy top
			ser.write(bytearray.fromhex(u'06')) 
			display.setCursorPosition(1, column)
			ser.write(bytearray.fromhex(u'07')) #candy bottom

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
	#display.setDisplayText('WiZard')

	# Animation test
	ser.write(lcdConstants.clearDisplay)
	loopCounter = 0
	while loopCounter < lcdConstants.numberOfChars:
		display.drawCandy(loopCounter)
		loopCounter = loopCounter + 1

	loopCounter = 0
	while loopCounter < lcdConstants.numberOfChars-2:
		display.drawPacmanOpen(loopCounter)
		time.sleep(1)
		display.drawPacmanClosed(loopCounter+1)
		display.setCursorPosition(0, loopCounter)
		display.setDisplayText(' ')
		display.setCursorPosition(1, loopCounter)
		display.setDisplayText(' ')
		time.sleep(1)
		loopCounter = loopCounter + 1
	ser.write(lcdConstants.clearDisplay)

	# display.drawPacmanClosed(14)
	# display.drawPacmanOpen(0)
	# display.drawCandy(2)
	# display.drawCandy(4)
	# display.drawCandy(6)
	# display.drawCandy(8)


	while True:
		pass