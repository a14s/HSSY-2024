import pigpio

def angle2pwm(angle):
	return int((((angle+90)/180)*2000)+500)
