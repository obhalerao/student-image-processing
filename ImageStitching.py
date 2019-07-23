import pathlib as pl
import numpy as np
import imutils
import cv2


filepath = 'random-images'

args = {"crop":1,
        "output":"stitched_image.jpg"}



imagePaths = pl.Path(filepath).iterdir()
images = []


for idx, imagePath in enumerate(imagePaths):
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

		cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
		cnts = imutils.grab_contours(cnts)
		c = max(cnts, key=cv2.contourArea)

		mask = np.zeros(thresh.shape, dtype="uint8")
		(x, y, w, h) = cv2.boundingRect(c)
		cv2.rectangle(mask, (x, y), (x + w, y + h), 255, -1)

		minRect = mask.copy()
		sub = mask.copy()
 
		while cv2.countNonZero(sub) > 0:
			minRect = cv2.erode(minRect, None)
			sub = cv2.subtract(minRect, thresh)

		cnts = cv2.findContours(minRect.copy(), cv2.RETR_EXTERNAL,
			cv2.CHAIN_APPROX_SIMPLE)
		cnts = imutils.grab_contours(cnts)
		c = max(cnts, key=cv2.contourArea)
		(x, y, w, h) = cv2.boundingRect(c)

		stitched = stitched[y:y + h, x:x + w]

	cv2.imwrite(args["output"], stitched)

	cv2.imshow("Stitched", stitched)
	cv2.waitKey(0)

else:
	print("[INFO] image stitching failed ({})".format(status))








