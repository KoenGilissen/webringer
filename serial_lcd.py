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

	time.sleep(1)		#display init delay

	LOG.info("Initializing LCD display")
	ser.write(lcdConstants.clearDisplay)
	ser.write(lcdConstants.turnOnDisplayCursorBlinking)
	ser.write(lcdConstants.cursorHomeLine0)

	LOG.info("Print some Text on the display")
	ser.write('Embedded Linux')
	ser.write(lcdConstants.cursorHomeLine1)
	ser.write('Wizard')
	while True:
		pass