#import modules
import smbus
import time

#setup SMBus
bus = smbus.SMBus(1)


_REG_SECONDS = 0x00
_REG_MINUTES = 0x01
_REG_HOURS = 0x02
_REG_DAY = 0x03
_REG_DATE = 0x04
_REG_MONTH = 0x05
_REG_YEAR = 0x06
_REG_CONTROL = 0x07

def _bcd_to_int(bcd):
    """Decode a 2x4bit BCD to a integer.
    """
    out = 0
    for d in (bcd >> 4, bcd):
        for p in (1, 2, 4 ,8):
            if d & 1:
                out += p
            d >>= 1
        out *= 10
    return int(out / 10)
    
#main loop
try:
	while 1:
		for counter in range(0, 255):   #the counter variable increments by 1 through to 255, then loops back to 0
			sec = _bcd_to_int(bus.read_byte_data(0x68, _REG_SECONDS))
			min = _bcd_to_int(bus.read_byte_data(0x68, _REG_MINUTES))
			d = bus.read_byte_data(0x68, _REG_HOURS)
			if d & 0x40:
				hour = _bcd_to_int(d & 0x3F)
			else:
				hour = _bcd_to_int(d & 0x1F)
				if d & 0x20:
					hour += 11  # Convert 12h to 24h
				elif hour == 12:
					hour = 0
			print("{0}:{1}:{2}".format(hour, min, sec))
			
			
			time.sleep(1)

except KeyboardInterrupt:   #when Ctrl   C is pressed, write all the LEDs off
    print("Program Exited Cleanly")
