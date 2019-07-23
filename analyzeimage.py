import cv2
import numpy as np

def analyzeimage(old_image):

        green_img = None #do some stuff to the image to get the green
        nir_img = None #do some stuff to the image to get the nir

        built_up_index = (green_img-2*nir_img)/(green_img+2*nir_img)

        built_up_index = cv2.fromarray(built_up_index)

        cv2.imwrite('static/temp.jpg', built_up_index)
        
	# analyze the image 'old_image' here
	# save the analyzed image to 'static/temp.jpg'
	# return the path of the new image file
	return "static/temp.jpg"
