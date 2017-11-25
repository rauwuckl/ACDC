from flask import Flask, render_template, session, request
import matplotlib.pyplot as plt
import numpy as np


import skimage.io
import skimage.exposure

import flask

app = Flask(__name__)
app.config['SECRET_KEY'] = '939fkj3kwlsk4958204kfjnkl39f9Ixne9l39((d'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/uploadImage', methods=['POST'])
def classifyImage():
    """classify and save the uploaded image"""

    file = request.files['file'];
    print(file)

    img = skimage.io.imread(request.files['file'])
    print(img.shape)
    norm_img = np.empty(img.shape)
    norm_img[:, :, 0] = skimage.exposure.equalize_hist(img[:, :, 0])
    norm_img[:, :, 1] = skimage.exposure.equalize_hist(img[:, :, 1])
    norm_img[:, :, 2] = skimage.exposure.equalize_hist(img[:, :, 2])

    bw = np.mean(img/np.max(img), axis=2)
    norm_bw = skimage.exposure.equalize_adapthist(bw)
    print("done")
    plt.imshow(norm_bw, cmap="Greys")
    plt.show()

    answer = None

    return flask.jsonify(answer)




if __name__ == '__main__':
    print('in my file')
    Flask.run(app, debug=False)
    print("ended gracefully")
