import cv2
import numpy as np

def analyzeimage(old_image):

        old_image_arr = np.array(old_image)

        nir_img = np.array[2]

        green_img = np.array[1] - nir_img

        built_up_index = (green_img-2*nir_img)/(green_img+2*nir_img)

        built_up_image = cv2.fromarray(built_up_index)

        cv2.imwrite('static/temp.jpg', built_up_image)
        
	# analyze the image 'old_image' here
	# save the analyzed image to 'static/temp.jpg'
	# return the path of the new image file
	return "static/temp.jpg"
