import cv2
from picamera2 import Picamera2

cam = Picamera2()
cam.start()

fourcc=cv2.VideoWriter_fourcc(*'XVID')
out=cv2.VideoWriter('output_old_v1.avi', fourcc,20.0, (640, 480))

i = 0
while True:
    try:
        frame = cv2.cvtColor(cam.capture_array(), cv2.COLOR_BGR2RGB)
        out.write(frame)
        i+=1
        print(i)
        #cv2.imshow("camera", frame)
    except:
        #cv2.imwrite("frame.png", frame)
        out.release()
        break
        #cv2.destroyAllWindows()

