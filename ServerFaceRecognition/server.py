import os
import cv2
import re
import base64
import numpy as np
from FaceRecognition import FaceRecognition
from PIL import Image
import face_recognition
from flask import Flask, render_template, flash, redirect, url_for, request
from flask_socketio import SocketIO, Namespace
from forms import RegistrationForm

def decode_base64(data, altchars=b'+/'):
    """Decode base64, padding being optional.

    :param data: Base64 data as an ASCII byte string
    :returns: The decoded byte string.

    """
    data = re.sub(rb'[^a-zA-Z0-9%s]+' % altchars, b'', data)  # normalize
    missing_padding = len(data) % 4
    if missing_padding:
        data += b'='* (4 - missing_padding)
    return base64.b64decode(data, altchars)

app = Flask (__name__)
app.config['SECRET_KEY'] = 'Secret!!'
socketio = SocketIO (app)
id = None

@app.route ('/')
@app.route ('/home')
def home() :
    return render_template ('home.html')

@socketio.on('connect', namespace='/public')
def call_front_end():
    socketio.emit('server_response', {'data':123}, namespace = '/public')

@app.route ('/recognize', methods=['GET', 'POST'])
def recognize() :
    encoded_img = request.form.get('encodedImg')
    path = None

    face = FaceRecognition()
    image = face.facerecognition(encoded_img)
    if image == 0 :
        return redirect (url_for('recognized_image'))

    return render_template ('recognize.html', path = path)

@app.route ('/recognized_image', methods=['GET', 'POST'])
def recognized_image () :
    path = "static/ServerToClient"
    image_type = "Image"
    counter = len([i for i in os.listdir(path) if image_type in i])
    path = url_for ('static', filename='ServerToClient/' + 'Image' + str (counter) + '.jpg')
    return render_template ('recognized_image.html', path=path)

def save_picture (form_picture, username) :
    path = "Dataset"
    path = os.path.abspath (path)
    image_type = "Image"
    image_counter = len([i for i in os.listdir(path) if image_type in i]) + 1

    image_name = "Image{}.jpg".format (image_counter)
    path = path + "/" + image_name

    img = Image.open (form_picture)
    img.save (path)

    file = open ("names.txt", "a+")
    file.write (username + "\n")
    file.close()

    print ("The ID number of " + username + "is : " + str (image_counter))

@app.route ('/register', methods=['GET', 'POST'])
def register() :
    form = RegistrationForm()
    if form.validate_on_submit () :

        picture_file = save_picture (form.picture.data, form.username.data)
        flash ('Successfuly uploaded the image of ' + form.username.data, 'success')
        return redirect (url_for ('home'))
    return render_template ('register.html', form = form)

if __name__ == '__main__' :
    socketio.run (app, port=8000, debug=True)
