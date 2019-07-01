import io
import os
import face_recognition
import numpy as np
import cv2
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, ValidationError
from wtforms.validators import DataRequired, Length, Email, EqualTo


class RegistrationForm (FlaskForm) :
    username = StringField ('Username', validators=[DataRequired(), Length(min=2, max=20)])
    picture = FileField ('Image', validators=[DataRequired(), FileAllowed(['jpg'])])
    submit = SubmitField ('Register')

    def validate_username (self, username) :
        file = open ("names.txt", "r+")
        for line in file.readlines() :
            print (line)
            if username.data == line[:-1] :
                raise ValidationError ("That username is taken. Please Choose a different Username")

        file.close()

    def validate_picture (self, picture) :
        if picture.data :
            in_memory_file = io.BytesIO()
            picture.data.save (in_memory_file)

            data = np.fromstring (in_memory_file.getvalue(), dtype=np.uint8)
            color_image_flag = 1
            img = cv2.imdecode (data, color_image_flag)

            path = os.path.abspath ('Dataset')
            image_type = "Image"
            image_counter = len([i for i in os.listdir(path) if image_type in i])
            path = 'Dataset/Image'

            face_encodings = face_recognition.face_encodings (img)
            for i in range (image_counter) :
                test_image = face_recognition.load_image_file (os.path.abspath (path + str (image_counter) + ".jpg"))
                test_encodings = face_recognition.face_encodings (test_image)

                matches = face_recognition.compare_faces (face_encodings, test_encodings[0])

                if True in matches :
                    raise ValidationError ("There is a similar image in the the Dataset.")

            if len (face_encodings) == 0 :
                print ("Validation error")
                raise ValidationError ("There is no face in this Image. Please try again!")
            elif len (face_encodings) > 1 :
                raise ValidationError ("There are more than one face in this image. Please try again!")
        else :
            raise ValidationError ("You should upload a image of the person that we need to recognize")
