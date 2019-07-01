import os
import face_recognition
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageEnhance

# To rotate a image by 90 degree in counter-clockwise direction
def rotate_image(img):
    return np.rot90 (img)

file = open (os.path.abspath ("RealTimeImages/names.txt"), "r")

# A list to store all the known Encodings
known_encodings = []
known_names = file.readlines()

# Counting the number of known images in the Encoded Folder
path = "RealTimeImages/EncodingImages"
image_type = "Image"
counter = len([i for i in os.listdir(path) if image_type in i])
print (counter)

# Getting all the Known Encoding
# All the photos should in Images/EncodingImages folder 
print ("Loading The Known Images....")
for i in range (counter) :
	path = "RealTimeImages/EncodingImages/Image" + str(i) + ".jpg"
	image = face_recognition.load_image_file (os.path.abspath(path))

	known_encoding = face_recognition.face_encodings (image)
	known_encodings.append (known_encoding[0])

cam = cv2.VideoCapture (0) 

path_to_save_images = "RealTimeImages/TestingImages/ImageType"

while True :
	ret, test_image = cam.read()

	recognized_id = []

	test_face_encodings = face_recognition.face_encodings (test_image)
	test_face_locations = face_recognition.face_locations (test_image)

	for test_face_encoding, test_face_location in list (zip (test_face_encodings, test_face_locations)) :
		matches = face_recognition.compare_faces (known_encodings, test_face_encoding)

		if True in matches :
			recognized_id.append ([i for i in range (len(matches)) if matches[i]])
		else :
			recognized_id.append ([-1])

		(top, right, bottom, left) = test_face_location

		if recognized_id [-1][0] == -1 :
			cropped_image = test_image[top-50:bottom+50, left-20:right+20]

			bright_cropped_image = (((test_image / 255.0) ** 0.5) * 255.0).astype ('uint8')
			dark_cropped_image = (((test_image / 255.0) ** 2.0) * 255.0).astype ('uint8')

			bright_face_encodings = face_recognition.face_encodings (bright_cropped_image)
			dark_face_encodings = face_recognition.face_encodings (dark_cropped_image)

			for bright_face_encoding, dark_face_encoding in list (zip (bright_face_encodings, dark_face_encodings)) :
				bright_matches = face_recognition.compare_faces (known_encodings, bright_face_encoding)
				dark_matches = face_recognition.compare_faces (known_encodings, dark_face_encoding)

				if True in bright_matches :
					recognized_id[-1] = [i for i in range (len(bright_matches)) if matches[i]]
					break

				if True in dark_matches :
					recognized_id[-1] = [i for i in range (len(dark_matches)) if matches[i]]
					break

		if recognized_id[-1][0] == -1 :
			enhance_image = Image.fromarray (test_image)
			enhance_image = ImageEnhance.Sharpness (enhance_image)
			enhance_image = enhance_image.enhance (2.5)
			
			test_face_encodings = face_recognition.face_encodings (np.array (enhance_image))

			for test_face_encoding in test_face_encodings :
				matches = face_recognition.compare_faces(known_encodings, test_face_encoding)

			if True in matches :
				recognized_id[-1] = [i for i in range (len(bright_matches)) if matches[i]]
				break

		if recognized_id[-1][0] == -1 :
			enhance_image = Image.fromarray (test_image)
			enhance_image = ImageEnhance.Contrast (enhance_image)
			enhance_image = enhance_image.enhance (2.5)
			
			test_face_encodings = face_recognition.face_encodings (np.array (enhance_image))

			for test_face_encoding in test_face_encodings :
				matches = face_recognition.compare_faces(known_encodings, test_face_encoding)

			if True in matches :
				recognized_id[-1] = [i for i in range (len(bright_matches)) if matches[i]]
				break

		try :
			if recognized_id[-1][0] == -1 :
				path = path_to_save_images + "_1"
			else :
				path = path_to_save_images + str (recognized_id[-1][0])
			counter = len([i for i in os.listdir(path) if image_type in i])
			path = path + "/Image" + str (counter) + ".jpg"

			cv2.imwrite (path, test_image[top-40:bottom+20, left-20:right+20])
		except Exception as e :
			if recognized_id[-1][0] == -1 :
				os.mkdir (path_to_save_images + "_1")
			else :
				os.mkdir (path_to_save_images + str (recognized_id[-1][0]))
			
			path = path + "/Image0.jpg"

			cv2.imwrite (path, test_image[top-40:bottom+20, left-20:right+20])


		cv2.rectangle(test_image, (left - 10, top - 40), (right + 10, bottom), (0, 205, 0), 2)
		
		font = cv2.FONT_HERSHEY_SIMPLEX
		if recognized_id[-1][0] == -1 :
			cv2.putText(test_image, "ID : Unknown", ((left + right) // 2 - 25, bottom + 15), font, 0.5, (0, 255, 0), 2, cv2.LINE_AA)
		else :
			cv2.putText(test_image, "ID : " + str (known_names [recognized_id[-1][0]][:-1]), ((left + right) // 2 - 25, bottom + 15), font, 0.5, (0, 255, 0), 2, cv2.LINE_AA)
		
	cv2.imshow ('Frame', test_image)

	k = cv2.waitKey (1) 

	if k % 256 == 32 :
		break

cam.release()

cv2.destroyAllWindows()
