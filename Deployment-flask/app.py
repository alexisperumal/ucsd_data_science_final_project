import numpy as np
from flask import Flask, request, jsonify, render_template
from sklearn.externals import joblib

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/LR')
def LR():
    return render_template('LR.html')

@app.route('/RFC')
def RFC():
    return render_template('RFC.html')

@app.route('/comparison')
def comparison():
    return render_template('comparison.html')

@app.route('/predict', methods=['POST'])
def predict():
    
        
    '''
    For rendering results on Prediction HTML GUI
    '''
    model  = joblib.load('bloottest_RFC_selected_features.pkl')
    
    
    features = [x for x in request.form.values()]
    final_features = [np.array(features)]
    prediction = model.predict(final_features)
    predicted_value = prediction[0]
    if int(predicted_value)== 1: 
        prediction ='Positive'
    else: 
        prediction ='Negative'            

    return render_template('index.html', prediction_text=prediction)
    
@app.route('/predict_api',methods=['POST'])
def predict_api():
    '''
    For direct API calls request
    '''
    
    model  = joblib.load('bloottest_RFC_selected_features.pkl')
    data = request.get_json(force=True)
    prediction = model.predict([np.array(list(data.values()))])

    predicted_value = prediction[0]
    return jsonify(predicted_value)

if __name__ == "__main__":
    app.run(port=5000,debug=True)