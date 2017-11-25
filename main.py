from flask import Flask, render_template, session, request
import matplotlib.pyplot as plt
import numpy as np

import backend.Vision_Mockup as vision

from io import BytesIO


import skimage.io
import skimage.exposure

import flask

app = Flask(__name__)
app.config['SECRET_KEY'] = '939fkj3kwlsk4958204kfjnkl39f9Ixne9l39((d'


global patient_pictures
patient_pictures = dict()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/uploadImage', methods=['POST'])
def classifyImage():
    """classify and save the uploaded image"""
    print("classifyImage")
    print(request)
    # request.get_data()
    # request.data
    print(request.headers)


    # file = request.files['file'];
    raw_data = request.data
    file_pointer = BytesIO(raw_data)

    img = skimage.io.imread(file_pointer) #request.files['file'])
    # plt.imshow(img, cmap="Greys")
    # plt.show()

    patient_id, distress = vision.get_person_id_and_distress(img)

    patient_pictures[patient_id] = img

    answer = {'status': 'doctor_coming'}

    return flask.jsonify(answer)

@app.route('/api/patientInfo/<patient_id>')
def display_patient_info(patient_id):


    pass





if __name__ == '__main__':
    print('in my file')
    Flask.run(app, debug=False)
    print("ended gracefully")
