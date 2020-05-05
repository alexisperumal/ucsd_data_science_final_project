import numpy as np
from flask import Flask, request, jsonify, render_template
from sklearn.externals import joblib

app = Flask(__name__)
model  = joblib.load('bloottest_RFC_selected_features.pkl')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/LR')
def LR():
    return render_template('LR.html')

@app.route('/RFC')
def RFC():
    return render_template('RFC.html')

if __name__ == "__main__":
    app.run(debug=True)