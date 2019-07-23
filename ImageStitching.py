import pathlib as pl
import numpy as np
import imutils
import cv2


filepath = 'random-images'



imagePaths = pl.Path(filepath).iterdir()
images = []


for imagePath in imagePaths:
        image = cv2.imread(str(imagePath))
        images.append(image)

print("[INFO] stitching images...")
stitcher = cv2.createStitcher() if imutils.is_cv3() else cv2.Stitcher_create()
(status, stitched) = stitcher.stitch(images)

if status == 0:
	if args["crop"] > 0:
		print("[INFO] cropping...")
		stitched = cv2.copyMakeBorder(stitched, 10, 10, 10, 10,
			cv2.BORDER_CONSTANT, (0, 0, 0))
		gray = cv2.cvtColor(stitched, cv2.COLOR_BGR2GRAY)
		thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY)[1]

