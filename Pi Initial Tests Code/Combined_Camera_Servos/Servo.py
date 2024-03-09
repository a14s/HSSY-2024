import pigpio

pi = pigpio.pi()

def angle2pwm(angle):
	return int((((angle+90)/180)*2000)+500)

class MyServo():
	def __init__(self, pin_num, init_pos=0):
		self.pin_num = pin_num
		self.init_pos = init_pos
		self.current_pos = 0
	def init_servo(self):
		pi.set_mode(self.pin_num, pigpio.OUTPUT)
		pi.set_servo_pulsewidth(self.pin_num, angle2pwm(self.init_pos))
		self.current_pos = self.init_pos
	def go_to(self, angle):
		pi.set_servo_pulsewidth(self.pin_num, angle2pwm(angle))
		self.current_pos = angle
	def go_by(self, angle):
		pi.set_servo_pulsewidth(self.pin_num, angle2pwm(self.current_pos+angle))
		self.current_pos += angle

