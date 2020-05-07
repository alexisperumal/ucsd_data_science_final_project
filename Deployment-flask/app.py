from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
from sklearn.externals import joblib
import numpy as np
from sklearn.externals import joblib

# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
# Database
app.config['SQLALCHEMY_DATABASE_URI'] = ('sqlite:///' + 
    os.path.join(basedir, 'db.sqlite'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Init db
db = SQLAlchemy(app)
# Init ma
ma = Marshmallow(app)

# Product Class/Model
class Predict(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_age_quantile = db.Column(db.Integer)
    leukocytes = db.Column(db.Float)
    platelets = db.Column(db.Float)
    monocytes = db.Column(db.Float)
    hematocrit = db.Column(db.Float)
    eosinophils  = db.Column(db.Float)
    red_blood_cells = db.Column(db.Float)
    hemoglobin = db.Column(db.Float)
    lymphocytes = db.Column(db.Float)
    mean_platelet_volume = db.Column(db.Float)

    def __init__(self, patient_age_quantile, leukocytes, platelets,
        monocytes, hematocrit, eosinophils, red_blood_cells,
        hemoglobin, lymphocytes, mean_platelet_volume):
        self.patient_age_quantile = patient_age_quantile
        self.leukocytes = leukocytes
        self.platelets = platelets
        self.monocytes = monocytes
        self.hematocrit = hematocrit
        self.eosinophils = eosinophils
        self.red_blood_cells = red_blood_cells
        self.hemoglobin = hemoglobin
        self.lymphocytes = lymphocytes
        self.mean_platelet_volume = mean_platelet_volume

class PredictSchema(ma.Schema):
    class Meta:
        fields = ('id', 'patient_age_quantile', 'leukocytes', 'platelets',
            'monocytes', 'hematocrit', 'eosinophils', 'red_blood_cells',
            'hemoglobin', 'lymphocytes', 'mean_platelet_volume')

predict_schema = PredictSchema()
predicts_schema = PredictSchema(many = True)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/LR')
def LR():
    return render_template('LR.html')

@app.route('/RFC')
def RFC():
    return render_template('RFC.html')

@app.route('/SVC')
def SVC():
    return render_template('SVC.html')

@app.route('/comparison')
def comparison():
    return render_template('comparison.html')


# Create a Product
@app.route('/predict', methods=['POST','GET'])
def predict():
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

    prediction = Predict(patient_age_quantile, leukocytes, platelets,
            monocytes, hematocrit, eosinophils, red_blood_cells,
            hemoglobin, lymphocytes, mean_platelet_volume)
    
    print(prediction)

    db.session.add(prediction)
    db.session.commit()
    print(predict_schema.jsonify(prediction)) 
    
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
    
    final_features = [np.array(features)]
    prediction = model.predict(final_features)
    predicted_value = prediction[0]
    if int(predicted_value)== 1: 
        prediction_resp ='Positive'
    else: 
        prediction_resp ='Negative'  
                 

    return render_template('index.html', prediction_text=prediction_resp)
    



# Run Server
if __name__ == '__main__':
    app.run(debug=True)
