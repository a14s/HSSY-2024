from PID import PID
from Servo import *
import pigpio
import time

direction = -1

pi = pigpio.pi()

pi.set_mode(18, pigpio.OUTPUT)
pi.set_mode(23, pigpio.OUTPUT)

pid = PID(kP=0.8, kI=0.05, kD=0)
pid.initialize()

current=-45-12
desired=-90
pi.set_servo_pulsewidth(18, angle2pwm(current))
pi.set_servo_pulsewidth(23, angle2pwm(0))

i = 0
while False: #True: #abs(current - desired) > 0:
	gain = pid.update(desired - current)
	if abs(current+gain)<90:
		current=current+gain
	print(current, desired, gain, angle2pwm(int(current)))
	print(direction)
	pi.set_servo_pulsewidth(18, angle2pwm(int(current)))
	print(current)
	#time.sleep(50/1000)
	i+=1
	if (direction == 1 and current > 85) or (direction == -1 and current < -85):
		direction*=-1
		desired*=-1
		gain=0
		time.sleep(2)
