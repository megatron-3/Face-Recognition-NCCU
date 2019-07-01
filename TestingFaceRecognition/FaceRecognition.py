import face_recognition
import os
import numpy as np
from PIL import Image, ImageEnhance

# To rotate a image by 90 degree in counter-clockwise direction
def rotate_image(img):
    return np.rot90 (img)

# A list to store all the known Encodings
known_encodings = []

# Getting all the Known Encoding
# All the photos should in Images/EncodingImages folder 
print ("Loading The Known Images....")
for i in range (6) :
	path = 'Images/EncodingImages/Image' + str (i) + '.jpg'
	image = face_recognition.load_image_file (os.path.abspath(path))

	known_encoding = face_recognition.face_encodings (image)
	known_encodings.append (known_encoding[0])

positive = 0
negative = 0

# Images to be tested
print ()
for i in range (6) :
	positive = 0
	negative = 0

	print ("Loading The Images of Type " + str (i+1) + "\n")
	for j in range (1000) :
		
		path = 'Images/TestingImages/ImageType' + str(i) + '/Image'
		path = path + str (j) + '.jpg'
		
		try :
			test_image = face_recognition.load_image_file (os.path.abspath (path))
			
			flag = 0

			for k in range (4) :
				test_face_encodings = face_recognition.face_encodings (test_image)

				for test_face_encoding in test_face_encodings :
					matches = face_recognition.compare_faces(known_encodings, test_face_encoding)

					if matches[i] :
						positive = positive + 1
						print ("Image " + str (j) + " of Image Type " + str (i + 1) + " is matched")
						flag = 1
						break
					else :
						continue

				if flag == 1 :
					break

				bright_test_image = (((test_image / 255.0) ** 0.5) * 255.0).astype ('uint8')
				dark_test_image = (((test_image / 255.0) ** 2.0) * 255.0).astype ('uint8')

				test_face_encodings = face_recognition.face_encodings (bright_test_image)
				test_face_encodings.extend (face_recognition.face_encodings (dark_test_image))

				for test_face_encoding in test_face_encodings :
					matches = face_recognition.compare_faces(known_encodings, test_face_encoding)

					if matches[i] :
						positive = positive + 1
						print ("Image " + str (j) + " of Image Type " + str (i + 1) + " is matched")
						flag = 1
						break
					else :
						continue

				test_image = rotate_image (test_image)

				if flag == 1 :
					break
			if flag == 0 :
				enhance_image = Image.fromarray (test_image)
				enhance_image = ImageEnhance.Sharpness (enhance_image)
				enhance_image = enhance_image.enhance (2.5)
				test_face_encodings = face_recognition.face_encodings (np.array (enhance_image))

				for test_face_encoding in test_face_encodings :
					matches = face_recognition.compare_faces(known_encodings, test_face_encoding)

					if matches[i] :
						positive = positive + 1
						print ("Image " + str (j) + " of Image Type " + str (i + 1) + " is matched")
						flag = 1
						break
					else :
						continue

			if flag == 0 :
				enhance_image = Image.fromarray (test_image)
				enhance_image = ImageEnhance.Contrast (enhance_image)
				enhance_image = enhance_image.enhance (2.5)
				test_face_encodings = face_recognition.face_encodings (np.array (enhance_image))

				for test_face_encoding in test_face_encodings :
					matches = face_recognition.compare_faces(known_encodings, test_face_encoding)

					if matches[i] :
						positive = positive + 1
						print ("Image " + str (j) + " of Image Type " + str (i + 1) + " is matched")
						flag = 1
						break
					else :
						continue

			if flag == 0:
				negative = negative + 1
				print ("Image " + str (j) + " of Image Type " + str (i + 1) + " is not matched")
				print ("The number of faces Found in the Image " + str (j) + " : " + str (len (test_face_encodings)))

		except Exception as e :
			print (e)

	print ()
	print ("The Total number of images correctly labelled : " + str (positive))
	print ("The total number of images in correctly labelled : " + str (negative))
	print ("The Total number of images Read : " + str (positive + negative))
	print ("Acuracy = " + str (positive * 100.0 / (positive + negative)) + "%")