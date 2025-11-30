from flask import Flask,render_template,request,redirect
from helper import preprocessing,vectorizer,get_prediction
from logger import logging

app = Flask(__name__)

logging.info("Flask App Started")
data = dict()
reviews = []
positive_reviews = 0
negative_reviews = 0

@app.route('/')
def index():
    data['reviews'] = reviews
    data['positive_reviews'] = positive_reviews
    data['negative_reviews'] = negative_reviews

    logging.info(f"================ Opening Home Page =================")
    return render_template('index.html', data=data)

@app.route("/",methods = ['post'])
def my_post():
    text = request.form['text']
    logging.info(f"Received review: {text}")
    preprocess_text = preprocessing(text)
    logging.info(f"Preprocessed review: {preprocess_text}")
    vectorized = vectorizer(preprocess_text)
    logging.info(f"Vectorized review: {vectorized}")
    prediction = get_prediction(vectorized)
    logging.info(f"Prediction result: {prediction}")
     
    if prediction == 'negative':
        global negative_reviews 
        negative_reviews += 1
    else:
        global positive_reviews
        positive_reviews += 1
    reviews.insert(0, text)
    return redirect(request.url)
        

if __name__ == "__main__":
    app.run()