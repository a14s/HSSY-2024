from image_processing import *
print("imported image processing")
from picamera2 import Picamera2
print("imported camera")
import time
import traceback
from Servo import MyServo
print("imported servo")
cam = Picamera2()
cam.start()

FOV_X, FOV_Y = 53, 41

vertical_servo = MyServo(18, -45)
vertical_servo.init_servo()
time.sleep(1)
horizontal_servo = MyServo(23, 0)
horizontal_servo.init_servo()
time.sleep(1)
command_servo=True #False
while True:
	try:
		t = time.time()
		# Adjusting Frame
		img = cam.capture_array()
		img = cv2.flip(img, 0)
		orig_h, orig_w = img.shape[:2]
		cv_corrected_img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
		for_processing = cv2.resize(cv_corrected_img.copy(), (orig_w//4, orig_h//4))
		# Getting desired color
		hsv = bgr2hsv(for_processing)
		mask = color_range(hsv, red=True)
		cv2.imshow("mask", mask)
		cv2.waitKey(1)
		coords = np.argwhere(mask)
		if len(coords) == 0:
			print("no color found")
			continue
		clusters = cluster_coords(coords, 1, 5)
		if np.max(clusters) == -1:
			print("no clusters found")
			continue
		# Remove Outliers
		non_outlier = clusters != -1
		clusters = clusters[non_outlier]
		coords = coords[non_outlier]
		largest_cluster = stats.mode(clusters)[0]
		# Obtain Rectangle
		desired_coords = coords[clusters == largest_cluster]
		y, x = desired_coords.T
		xyxy = np.array([x.min(), y.min(), x.max(), y.max()])*4
		# Calculate Error
		center_x = ((xyxy[2] - xyxy[0])//2) + xyxy[0]
		center_y = ((xyxy[3] - xyxy[1]))//2 + xyxy[1]
		degree_error_x = ((center_x - (orig_w//2))/orig_w)*FOV_X
		degree_error_y =   ((center_y - (orig_h//2))/orig_h)*FOV_Y
		if abs(degree_error_y) < 15 and command_servo: 
			vertical_servo.go_by(-1*degree_error_y/3)
			time.sleep(25/1000)
		if abs(degree_error_x) < 15 and command_servo:
			horizontal_servo.go_by(degree_error_x/3)
			time.sleep(25/1000)
		print("Errors: ", degree_error_x, degree_error_y)
		# Translate to servo language
		# Send to Servo
		# Visualization
		print("fps: ", 1/(time.time() - t))
		for_vis = cv_corrected_img.copy()
		cv2.circle(for_vis, (int(center_x), int(center_y)), 3, (0, 255, 0), 2)
		cv2.rectangle(for_vis, (int(xyxy[0]), int(xyxy[1])), (int(xyxy[2]), int(xyxy[3])), (0, 255, 0), 2) 
		cv2.imshow("feed", for_vis)
		if cv2.waitKey(1) == ord('q'):
			break
	except Exception as e:
		print(traceback.format_exc())
		cv2.destroyAllWindows()
		break
