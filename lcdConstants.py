#lcdConstants

# controlCharacter 'FE'
#8 bit values in byte array are seperated by a single space
clearDisplay = bytearray.fromhex(u'FE 01') #  Clear Display
moveCursorRight = bytearray.fromhex(u'FE 14')	 #  Move Cursor Right 1 Space
moveCursorLeft = bytearray.fromhex(u'FE 10')	 #  Move Cursor Left 1 Space
scrollRight = bytearray.fromhex(u'FE 1C')	 #  Scroll Right 1 Space
scrollLeft = bytearray.fromhex(u'FE 18')	 #  Scroll Left 1 Space
turnOffDisplay = bytearray.fromhex(u'FE 08')	 # Turn Display Off
turnOnDisplay = bytearray.fromhex(u'FE 0C')	 #  Turn Display On / Cursor Off / Blinking Off
turnOnDisplayCursor = bytearray.fromhex(u'FE 0E')	 #  Turn Display On / Cursor on / Blinking Off
turnOnDisplayCursorBlinking = bytearray.fromhex(u'FE 0F')	 #  Turn Display On / Cursor on / Blinking On
underlineCursor = bytearray.fromhex(u'FE 0E')	 #  Underline Cursor On
blinkCursor = bytearray.fromhex(u'FE 0D')	 #  Blinking Cursor On
cursorHomeLine0 = bytearray.fromhex(u'FE 80')	 # DD ram address 0x00 (128)
cursorHomeLine1 = bytearray.fromhex(u'FE C0')	 # DD ran address 0x40 (192)
turnOffDisplayShift = bytearray.fromhex(u'FE 10')