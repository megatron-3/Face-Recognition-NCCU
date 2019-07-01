import os
import face_recognition

image_type = input ('Image Type : ')
first = int (input ('Number of images to be labelled : '))
second_1 = int (input ('Starting index of extra images : '))
second_2 = int (input ('Ending index of extra images : '))

path = 'Images/TestingImages/ImageType' + image_type + '/Image'
for i in range (first) :
	try :
		des_image_path = path + str (i) + '.jpg'
		image = face_recognition.load_image_file (os.path.abspath (des_image_path))
	except Exception as e :
		print ('Did not found Image ' + str (i))
		for j in range (second_1, second_2) :
			try :
				source_image_path = path + str (j) + '.jpg'
				image = face_recognition.load_image_file (os.path.abspath (source_image_path))
				os.rename (source_image_path, des_image_path)
				print ("Placing Image " + str (j))
				break
			except Exception as e:
				continue