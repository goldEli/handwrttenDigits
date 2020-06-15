'''
@Author: miaoyu
@Date: 2020-06-15 22:23:28
@LastEditTime: 2020-06-15 22:41:01
@LastEditors: miaoyu
@Description: 
'''

from __future__ import absolute_import, division, print_function, unicode_literals
import tensorflow as tf
import numpy as np
from PIL import Image
from matplotlib import pyplot as plt
import cv2
from flask import Flask, jsonify, render_template, request, send_from_directory

import base64

mnist = tf.keras.datasets.mnist # Object of the MNIST dataset
(x_train, y_train),(x_test, y_test) = mnist.load_data() # Load data

# Normalize the train dataset
x_train = tf.keras.utils.normalize(x_train, axis=1)
# Normalize the test dataset
x_test = tf.keras.utils.normalize(x_test, axis=1)

#Build the model object
model = tf.keras.models.Sequential()
# Add the Flatten Layer
model.add(tf.keras.layers.Flatten())
# Build the input and the hidden layers
model.add(tf.keras.layers.Dense(128, activation=tf.nn.relu))
model.add(tf.keras.layers.Dense(128, activation=tf.nn.relu))
# Build the output layer
model.add(tf.keras.layers.Dense(10, activation=tf.nn.softmax))

# Compile the model
model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])

model.fit(x=x_train, y=y_train, epochs=5) # Start training process

model.save('re_model')

# Evaluate the model performance
test_loss, test_acc = model.evaluate(x=x_test, y=y_test)
# Print out the model accuracy 
print('\nTest accuracy:', test_acc)

def read_data(path):
#   img = base64.b64decode(msg.payload)
  image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
  processed_image = cv2.resize(image, dsize=(28,28))
  processed_image = np.resize(processed_image, new_shape=(1, 784))
  processed_image = processed_image/255.0
  return processed_image

img = read_data("./1.png")
# # print(img, img.shape)
# model = keras.models.load_model('re_model')
predictions = model.predict([[img]]) # Make prediction
print(np.argmax(predictions[0])) # Print out the number
