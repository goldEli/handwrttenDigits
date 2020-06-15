'''
@Author: miaoyu
@Date: 2020-06-15 22:08:00
@LastEditTime: 2020-06-15 23:05:39
@LastEditors: miaoyu
@Description: 
'''
from __future__ import absolute_import, division, print_function, unicode_literals
from tensorflow import keras

import numpy as np
from PIL import Image
from matplotlib import pyplot as plt
import cv2
from flask import Flask, jsonify, render_template, request, send_from_directory

import base64

def read_data(path):
#   img = base64.b64decode(msg.payload)
  image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
  processed_image = cv2.resize(image, dsize=(28,28))
  processed_image = np.resize(processed_image, new_shape=(1, 784))
  processed_image = processed_image/255.0
  return processed_image

def readb64(base64_string):
    # sbuf = StringIO()
    # sbuf.write(base64.b64decode(base64_string))
    # pimg = Image.open(sbuf)
    # return cv2.cvtColor(np.array(pimg), cv2.IMREAD_GRAYSCALE)
    img_data = base64.b64decode(base64_string)
    nparr = np.fromstring(img_data, np.uint8)
    img_np = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)
    processed_image = cv2.resize(img_np, dsize=(28,28))
    processed_image = np.resize(processed_image, new_shape=(1, 784))
    processed_image = processed_image/255.0
    return processed_image

# webapp
app = Flask(__name__,static_url_path='', static_folder='../')

@app.route('/')
def main():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/recognize', methods=['GET', 'POST'])
def recognize():
    image_string = request.json['img']
    img = readb64(image_string)
    # print(123, img_np.shape)

    # img = read_data("./mnist_png/testing/9/9.png")
    # print(img.shape)
    model = keras.models.load_model('re_model')
    predictions = model.predict(img) # Make prediction
    p = np.argmax(predictions[0]) # Print out the number
    print(p)
    return jsonify({"predictions": str(p)})


if __name__ == '__main__':

    app.run(port=8008, debug=True)
