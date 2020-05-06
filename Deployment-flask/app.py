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

@app.route('/predict', methods=['POST','GET'])
def predict():
    
        
    '''
    For rendering results on Prediction HTML GUI
    '''
    model  = joblib.load('bloottest_RFC_selected_features.pkl')
    patient_age_quantile = int(request.form.get('patient_age_quantile'))
    leukocytes = float(request.form.get('leukocytes'))
    platelets = float(request.form.get('platelets'))
    monocytes = float(request.form.get('monocytes'))
    hematocrit = float(request.form.get('hematocrit'))
    eosinophils = float(request.form.get('eosinophils'))
    red_blood_cells = float(request.form.get('red_blood_cells'))
    hemoglobin = float(request.form.get('hemoglobin'))
    lymphocytes = float(request.form.get('lymphocytes'))
    mean_platelet_volume = float(request.form.get('mean_platelet_volume'))

    print(patient_age_quantile, leukocytes)
    print(type(patient_age_quantile), type(leukocytes))
    
    features = [ 
                patient_age_quantile, 
                leukocytes,
                platelets,
                monocytes,
                hematocrit,
                eosinophils,
                red_blood_cells,
                hemoglobin,
                lymphocytes,
                mean_platelet_volume]
    
    
    #features = [x for x in request.form.values()] // text format
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