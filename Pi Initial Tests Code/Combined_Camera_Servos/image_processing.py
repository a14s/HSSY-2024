import cv2
import numpy as np
from scipy import stats
from sklearn.cluster import DBSCAN

def bgr2hsv(img):
	return cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

def color_range(hsv_img, hsv_low=np.array([110, 50, 50]), hsv_high=np.array([180, 255, 255]), red=False):
	if red:
		lower_red = np.array([0,40,190])
		upper_red = np.array([60,255,255])
		mask0 = cv2.inRange(hsv_img, lower_red, upper_red)

		lower_red = np.array([170,40,190])
		upper_red = np.array([180,255,255])
		mask1 = cv2.inRange(hsv_img, lower_red, upper_red)
		return mask0+mask1
	else:
		return cv2.inRange(hsv_img, hsv_low, hsv_high)

def cluster_coords(coords, eps=5, min_samples=15):
	clustering = DBSCAN(eps=eps, min_samples=min_samples).fit(coords)
	return clustering.labels_
