import pickle
from model_detect.cleanData import text_preprocess
from model_detect.crawlData import crawl
from flask import Flask, request, jsonify




def preprocess_text(text):
    text = text_preprocess(text)
    return text


def extract_text_from_url(url):
    try:
        return crawl(url)
    except Exception as e:
        return str(e)
    
    
def detect_fakenews(url):
    MODEL_PATH = r".\model_detect\naive_bayes.pkl"
    model = pickle.load(open(MODEL_PATH, 'rb'))

    print(url)
    # Extract text content from URL
    text = extract_text_from_url(url)
    print(text)
    if  text:
        preprocessed_text = preprocess_text(text['content'])
        # Predict label using the model
        predicted_label = model.predict([preprocessed_text])[0]
        if predicted_label == 1:
            result = 'Safe news'
        else : result  = 'Danger news'

        return {'url': url,'content':text, 'predicted_label': result}