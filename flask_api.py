# -*- coding: utf-8 -*-
"""
Created on Sun May 17 20:36:11 2020

@author: degananda.reddy
"""

from flask import Flask, request,jsonify,render_template
import numpy as np
import pickle
from . import config
import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import load_model
from keras.preprocessing.text import Tokenizer
from keras.preprocessing import sequence
from healthcheck import HealthCheck
app=Flask(__name__)    
new_model = tf.keras.models.load_model('model.hdf5')

data = pickle.load( open( "tokens_data", "rb" ) )



@app.route('/')
def home():
	return render_template('index.html')

@app.route('/predict',methods=["POST"])
def predict():
    if request.method == 'POST':
        text = request.form['message']
        pred_data=pd.Series(text)
        max_words = 73738
        max_len = 128
        tokens=data['tokens']
        # using Tokenizer
        sequences = tokens.texts_to_sequences(pred_data)
        sequences_matrix = sequence.pad_sequences(sequences,maxlen=max_len)
        print(sequences_matrix)
        predictions=new_model.predict(sequences_matrix)
        return render_template('result.html', prediction=predictions)


if __name__=='__main__':
    app.run(host="0.0.0.0", port=config.PORT, debug=config.DEBUG_MODE)