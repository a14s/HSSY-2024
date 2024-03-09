from image_processing import *
from picamera2 import Picamera2
import time
import traceback

cam = Picamera2()
cam.start()

while True:
	try:
		t = time.time()
		img = cam.capture_array()
		img = cv2.flip(img, 0)
		orig_h, orig_w = img.shape[:2]
		cv_corrected_img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
		for_processing = cv2.resize(cv_corrected_img.copy(), (orig_w//4, orig_h//4))
		hsv = bgr2hsv(for_processing)
		mask = color_range(hsv)
		cv2.imshow("mask", mask)
		cv2.waitKey(1)
		coords = np.argwhere(mask)
		if len(coords) == 0:
			print("no color found")
			continue
		clusters = cluster_coords(coords, 1, 5)
		if np.max(clusters) == -1:
			print("no clusters found")
			print(clusters)
			continue
		#remove outliers
		non_outlier = clusters != -1
		clusters = clusters[non_outlier]
		coords = coords[non_outlier]
		largest_cluster = stats.mode(clusters)[0]
		print(largest_cluster, np.max(clusters), clusters)
		desired_coords = coords[clusters == largest_cluster]
		y, x = desired_coords.T
		xyxy = np.array([x.min(), y.min(), x.max(), y.max()])*4
		print("fps: ", 1/(time.time() - t))
		for_vis = cv_corrected_img.copy()
		cv2.rectangle(for_vis, (int(xyxy[0]), int(xyxy[1])), (int(xyxy[2]), int(xyxy[3])), (0, 255, 0), 2) 
		cv2.imshow("feed", for_vis)
		if cv2.waitKey(1) == ord('q'):
			break
	except Exception as e:
		print(traceback.format_exc())
		cv2.destroyAllWindows()
		break
