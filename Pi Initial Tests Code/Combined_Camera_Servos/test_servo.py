from Servo import MyServo
import time
s = MyServo(18)
s.go_to(45)
time.sleep(2)
s.go_by(-20)
time.sleep(1)
print(s.current_pos)
