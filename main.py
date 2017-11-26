from io import BytesIO

import flask
from flask import Flask, render_template, request, send_file, abort, Response
from flask_mail import Mail, Message
from timeit import default_timer as timer

import src.Patient_Data as Patient_Data
import src.VisionAPI_Interface as Vision

domain = "http://127.0.0.1:5000/"

app = Flask(__name__)
app.config['SECRET_KEY'] = '939fkj3kwlsk4958204kfjnkl39f9Ixne9l39((d'

app.config.update(dict(
    DEBUG = True,
    MAIL_SERVER = 'smtp.strato.de',
    MAIL_PORT = 465,
    MAIL_USE_TLS = False,
    MAIL_USE_SSL = True,
    MAIL_USERNAME = 'pimpmypatient@brueckepfaffenstein.de',
    MAIL_PASSWORD = 'l3nJpKsTNulw4b3q'
))

mail = Mail(app)


global patient_pictures
patient_pictures = dict()

global patient_distress_levels
patient_distress_levels = dict()

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

    try:
        patient_id, distress = Vision.get_face_id(raw_data)
    except ValueError:
        print("No face in the image")
        resp = flask.jsonify({"message": "There was no face in the image."})
        resp.status_code = 400
        return resp
    except RuntimeError:

        print("no face recognised")
        resp = flask.jsonify({"message":"The Face wasn't recognised"})
        resp.status_code = 401
        return resp

    patient_pictures[patient_id] = raw_data
    patient_distress_levels[patient_id] = distress

    notifyDoctor(patient_id, distress)

    answer = {'status': 'doctor_coming', 'patient_id': patient_id}

    return flask.jsonify(answer)

@app.route('/api/patientImage/<patient_id>/<hacky_hash>')
def getPatientImage(patient_id, hacky_hash):
    try:
        raw_data = patient_pictures[patient_id]
        fp = BytesIO(raw_data)
        return send_file(fp, mimetype='image/jpeg')
    except KeyError:
        #do a error message here
        # TODO some error
        print("KeyError")


def notifyDoctor(patient_id, distress):
    header = "A patient needs you (Level {} pain)".format(distress)
    hacky_hash = timer() % 100000
    body = domain + "patientInfo/{}/{}".format(patient_id, hacky_hash)
    msg = Message(subject=header, sender="pimpmypatient@brueckepfaffenstein.de", body=body, recipients=["chutter@uos.de"])
    mail.send(msg)



@app.route('/patientInfo/<patient_id>/<hacky_hash>')
def display_patient_info(patient_id, hacky_hash):
    try:
        patient_data = Patient_Data.get_patient_data(patient_id)
    except ValueError:
        print("ladia")
        abort(404)



    distress = patient_distress_levels.get(patient_id, 0)
    return render_template('doctor_view.html', hacky_hash=hacky_hash, distress=distress, data=patient_data)# conditions=conditions, patient_id=patient_id, personal_details=personal_details)


if __name__ == '__main__':
    print('in my file')
    Flask.run(app, debug=False)
    print("ended gracefully")
