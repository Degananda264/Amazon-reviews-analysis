# -*- coding: utf-8 -*-
"""
Created on Sun May 17 20:36:11 2020

@author: degananda.reddy
"""

from flask import Flask, request,jsonify
import numpy as np
import pickle
import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import load_model
from keras.preprocessing.text import Tokenizer
from keras.preprocessing import sequence
from healthcheck import HealthCheck
import logging
app=Flask(__name__)    
new_model = tf.keras.models.load_model('model.hdf5')
data = pickle.load( open( "tokens_data", "rb" ) )
logging.basicConfig(filename="flask.log",level=logging.DEBUG,format='%(asctime)s %(levelname)s %(threadName)s : %(message)s')
logging.info('Model and Tokens Loaded....')
health=HealthCheck(app,"/check")

def howami():
    return True, "Iam a good"

health.add_check(howami)

def predict(pred_text):
  pred_data=pd.Series(pred_text)
  max_words = 73738
  max_len = 128
  tokens=data['tokens']
  # using Tokenizer
  sequences = tokens.texts_to_sequences(pred_data)
  sequences_matrix = sequence.pad_sequences(sequences,maxlen=max_len)
  print(sequences_matrix)
  predictions=new_model.predict(sequences_matrix)
  return (predictions.tolist())

        

#pred_text="Very Unhappy with product and delivery."
#predict(pred_text)


@app.route('/')
def welcome():
    return "Welcome All"

@app.route('/predict',methods=["Get"])
def predict_sentiment():
    text=request.args.get("text")
    print(text)
    pred=predict(text)
    sentiment="positive" if float(''.join(map(str,pred[0]))) > 0.60 else "negative"
    app.logger.info("prediction:"+str(pred[0]) + "sentiment:"+sentiment)
    return jsonify({'predictions':pred,'sentiment':sentiment})
    


if __name__=='__main__':
    app.run()