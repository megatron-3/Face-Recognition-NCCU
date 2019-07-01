import os
import cv2
import re
import io
import numpy as np
import face_recognition
import base64
from PIL import Image, ImageDraw, ImageEnhance

class FaceRecognition (object) :
    def decode_base64(self, data, altchars=b'+/') :
        data = re.sub(rb'[^a-zA-Z0-9%s]+' % altchars, b'', data)

        missing_padding = len(data) % 4
        if missing_padding:
            data += b'='* (4 - missing_padding)
        return base64.b64decode(data, altchars)

    def facerecognition (self, encoded_image) :
        if (encoded_image is None) :
            return 1
        image = base64.b64decode (encoded_image[22:])
        image_array = np.fromstring (image, np.uint8)
        self.image = cv2.imdecode (image_array, cv2.COLOR_BGR2RGB)

        file = open (os.path.abspath ("names.txt"), "r")

        known_encodings = []
        known_names = file.readlines()

        file.close ()

        counter = len (known_names)
        print ("Number of Known Encodings : " + str (counter))

        print ("Loading the known Images.....")
        for i in range (counter) :
            path = "Dataset/Image" + str (i+1) + ".jpg"
            image = face_recognition.load_image_file (os.path.abspath (path))

            known_encoding = face_recognition.face_encodings (image)
            known_encodings.append (known_encoding[0])

        recognized_id = []
        path_to_save_images = "Dataset/ImageType"
        image_type = "Image"

        test_face_encodings = face_recognition.face_encodings (self.image)
        test_face_locations = face_recognition.face_locations (self.image)

        for test_face_encoding, test_face_location in zip (test_face_encodings, test_face_locations) :
            matches = face_recognition.compare_faces (known_encodings, test_face_encoding)

            if True in matches :
                recognized_id.append ([i for i in range (len(matches)) if matches[i]])
            else :
                recognized_id.append ([-1])

            (top, right, bottom, left) = test_face_location

            if recognized_id [-1][0] == -1 :
                cropped_image = self.image[top-50:bottom+50, left-20:right+20]

                bright_cropped_image = (((self.image / 255.0) ** 0.5) * 255.0).astype ('uint8')
                dark_cropped_image = (((self.image / 255.0) ** 2.0) * 255.0).astype ('uint8')

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
                enhance_image = Image.fromarray (self.image)
                enhance_image = ImageEnhance.Sharpness (enhance_image)
                enhance_image = enhance_image.enhance (2.5)

                test_face_encodings = face_recognition.face_encodings (np.array (enhance_image))

                for test_face_encoding in test_face_encodings :
                    matches = face_recognition.compare_faces(known_encodings, test_face_encoding)

                if True in matches :
                    recognized_id[-1] = [i for i in range (len(bright_matches)) if matches[i]]
                    break

            if recognized_id[-1][0] == -1 :
                enhance_image = Image.fromarray (self.image)
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
                counter = len([i for i in os.listdir(path) if image_type in i]) + 1
                path = path + "/Image" + str (counter) + ".jpg"

                cv2.imwrite (path, self.image[top-40:bottom+20, left-20:right+20])
            except Exception as e :
                print (e)
                if recognized_id[-1][0] == -1 :
                    os.mkdir (path_to_save_images + "_1")
                else :
                    os.mkdir (path_to_save_images + str (recognized_id[-1][0]))

                path = path + "/Image0.jpg"

                cv2.imwrite (path, self.image[top-40:bottom+20, left-20:right+20])

            cv2.rectangle(self.image, (left - 10, top - 40), (right + 10, bottom), (0, 205, 0), 2)

            font = cv2.FONT_HERSHEY_SIMPLEX
            if recognized_id[-1][0] == -1 :
                cv2.putText(self.image, "ID : Unknown", ((left + right) // 2 - 25, bottom + 15), font, 0.5, (0, 255, 0), 2, cv2.LINE_AA)
            else :
                cv2.putText(self.image, "ID : " + str (known_names [recognized_id[-1][0]][:-1]), ((left + right) // 2 - 25, bottom + 15), font, 0.5, (0, 255, 0), 2, cv2.LINE_AA)

            path = "static/ServerToClient"
            counter = len([i for i in os.listdir(path) if image_type in i]) + 1
            path = path + "/Image" + str (counter) + ".jpg"
            cv2.imwrite (os.path.abspath (path), self.image)
        return 0
