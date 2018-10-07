import os
import io
from io import BytesIO

from time import time
from flask.helpers import send_file
import numpy as np
import json
from PIL import Image
import skimage.io
#from service import load_model

import test_combine_service as t

import base64
import json
import requests
import flask
from flask import Flask, globals, request, g, jsonify

app = Flask(__name__)

def do_inference(image):
    res = t.main(image)
    print('prediction working...')
    return res


@app.route('/predict', methods=['POST'])
def predict():

    global m
    # process the first file only
    uploaded_files = globals.request.files.getlist('file')
    print('printing... {}'.format(uploaded_files))
    #data = uploaded_files[0].read()
    image = skimage.io.imread(uploaded_files[0])
    #image = Image.open(io.BytesIO(data))
    print('Image type {}'.format(type(image)))
    start_time = time()

##    image = adjust_image(image)
##    print('Image type {}'.format(type(image)))
    results = do_inference(image)

    print('total time taken = {}'.format(time()-start_time))

    return jsonify(results)

port = os.getenv('PORT', '5008')
if __name__ == "__main__":
    t.setup()
    app.debug = not os.getenv('PORT')
    app.run(host='0.0.0.0', debug=False, port=int(port))


