import pickle
from .model_detect.cleanData import text_preprocess
from .model_detect.crawlData import crawl
from flask import Flask, request, jsonify

import os

basedir = os.path.abspath(os.path.dirname(__file__))

def preprocess_text(text):
    text = text_preprocess(text)
    return text


def extract_text_from_url(url):
    try:
        return crawl(url)
    except Exception as e:
        return str(e)
    
    
def detect_fakenews(url):
    MODEL_PATH = os.path.join(basedir, r"model_detect/naive_bayes.pkl")
    model = pickle.load(open(MODEL_PATH, 'rb'))


    # Extract text content from URL
    text = extract_text_from_url(url)
    
    if  text:
        preprocessed_text = preprocess_text(text['content'])
        # Predict label using the model
        predicted_label = model.predict([preprocessed_text])[0]
        if predicted_label == 1:
            result = 'Safe news'
        else : result  = 'Danger news'
        
        text['predicted_label'] = result
        
        return text