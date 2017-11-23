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
cursorHomeLine1 = bytearray.fromhex(u'FE C0')	 # DD ram address 0xC0 (192)
turnOffDisplayShift = bytearray.fromhex(u'FE 10')

#Custom Chars
pacman0 = bytearray.fromhex(u'00 00 00 01 07 0F 0F 1F')
pacman1 = bytearray.fromhex(u'00 00 00 10 1c 0e 1e 1f')
pacman2 = bytearray.fromhex(u'1f 0f 0f 07 01 00 00 00')
pacman3 = bytearray.fromhex(u'1f 1e 1e 1c 10 00 00 00')
pacman4 = bytearray.fromhex(u'00 00 00 10 1c 0e 1c 10')
pacman5 = bytearray.fromhex(u'10 1c 1e 1c 10 00 00 00')


#CGROM addresses
cgramChar0Base =  64 # 0x40
cgramChar1Base =  72 #  0x48
cgramChar2Base =  80 #  0x50
cgramChar3Base =  88 #  0x58
cgramChar4Base =  96 #  0x60
cgramChar5Base =  104 #  0x68
cgramChar6Base =  112 #  0x70
cgramChar7Base =  120 #  0x78