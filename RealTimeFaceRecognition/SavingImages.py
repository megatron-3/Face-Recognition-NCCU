import os
import cv2
import face_recognition

cam = cv2.VideoCapture(0)

cv2.namedWindow("Capturing Images....")

path = "RealTimeImages/EncodingImages"
image_type = "Image"
image_counter = len([i for i in os.listdir(path) if image_type in i])

flag = 0

file = open (os.path.abspath ("RealTimeImages/names.txt"), "a+")

while flag == 0:
	ret, frame = cam.read()
	cv2.imshow("Capturing Images....", frame)

	encodings = face_recognition.face_encodings (frame)

	if len(encodings) == 1 :
		print ("Press Space when you want to record the image")

		k = cv2.waitKey (0)

		if k % 256 == 32 :
			known_face_encodings = []
			path_known = "RealTimeImages/EncodingImages/Image"

			counter = len([i for i in os.listdir(path) if image_type in i])
			for i in range (counter) :
				path_known = "RealTimeImages/EncodingImages/Image"
				path_known += str (i) + ".jpg"
				print (path_known)
				known_image = face_recognition.load_image_file (os.path.abspath (path_known))
				known_face_encodings = face_recognition.face_encodings (known_image)

			flag2 = 0
			for encoding in encodings :
				matches = face_recognition.compare_faces (known_face_encodings, encoding)

				if True in matches :
					print ("The Person Is already saved in the database")
					flag2 = 1
			if flag2 == 0 :
				print ("Enter the Name of the person")
				name = input ()

				image_name = "Image{}.jpg".format(image_counter)
				path = path + "/" + image_name
				
				cv2.imwrite(os.path.abspath (path), frame)
				print("{} written!".format(image_name))
				
				image_counter += 1
				flag = 1

				file.write (name + "\n")

	elif len (encodings) == 0 :
		print ("Cannot find a Face in the image")
		print ("Press Escape when you there is a face in front of the screen")

		k = cv2.waitKey (0)

		if k % 256 == 27 :
			print ("Capturing the image again")
	else :
		print ("More than 1 Faces are in front of the screen")
		print ("Press Escape when there is only 1 person in front of the screen")

		k = cv2.waitKey (0)

		if k % 256 == 27 :
			print ("Capturing the image again")

file.close ()

cam.release()

cv2.destroyAllWindows()
