from RaadGS import *

gs = RaadGS()
frame = np.array([])
#cap = cv2.VideoCapture(0)
while True:
    #ret, frame = cap.read()
    gs.render(frame)
    if cv2.waitKey(20) == ord('q'):
        break