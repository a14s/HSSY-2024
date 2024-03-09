import cv2
import numpy as np
from picamera2 import Picamera2

cam = Picamera2()
cam.start()

def nothing(x):
    pass

def hsv_calc():
    cv2.namedWindow("Trackbars",)
    cv2.createTrackbar("lh","Trackbars",0,179,nothing)
    cv2.createTrackbar("ls","Trackbars",0,255,nothing)
    cv2.createTrackbar("lv","Trackbars",0,255,nothing)
    cv2.createTrackbar("uh","Trackbars",179,179,nothing)
    cv2.createTrackbar("us","Trackbars",255,255,nothing)
    cv2.createTrackbar("uv","Trackbars",255,255,nothing)
    while True:
        frame = cv2.flip(cv2.cvtColor(cam.capture_array(), cv2.COLOR_RGB2HSV), 0)
        #frame = cv2.imread('candy.jpg')
        height, width = frame.shape[:2]
        #frame = cv2.resize(frame,(width/5, height/5), interpolation = cv2.INTER_CUBIC)
        hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

        lh = cv2.getTrackbarPos("lh","Trackbars")
        ls = cv2.getTrackbarPos("ls","Trackbars")
        lv = cv2.getTrackbarPos("lv","Trackbars")
        uh = cv2.getTrackbarPos("uh","Trackbars")
        us = cv2.getTrackbarPos("us","Trackbars")
        uv = cv2.getTrackbarPos("uv","Trackbars")

        l_blue = np.array([lh,ls,lv])
        u_blue = np.array([uh,us,uv])
        mask = cv2.inRange(hsv, l_blue, u_blue)
        result = cv2.bitwise_or(frame,frame,mask=mask)

        #cv2.imshow("frame",frame)
        cv2.imshow("mask",mask)
        cv2.imshow("result",result)
        key = cv2.waitKey(1)
        if key == 27:
            break
    cv2.destroyAllWindows()

hsv_calc()
