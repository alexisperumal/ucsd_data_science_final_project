from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
import joblib
import numpy as np
from flask import Flask, request, jsonify, render_template
from sklearn.preprocessing import StandardScaler


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

#------- use the function if model saved is scaled)------#
def scaleInput(inputArray):
    reshaped = np.array(inputArray).reshape(1,-1)
    x_scaler = StandardScaler().fit(reshaped)
    return x_scaler.transform(reshaped)
#------- use the function if model saved is scaled)------#    

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/LR')
def LR():
    n1 = ['Total Patients', 'Negative COVID-19 Patients',
        'Positive COVID-19 Patients']
    v1 = [598, 517, 81]

    n2 = ['Total Patient Training Data',
        'Total Patient Testing Data']
    v2 = [448, 150]

    n3 = ['Accuracy', 'Precision', 'Recall']
    result = ['93.3%', '80.0%', '63.2%']
    return render_template('LR.html',
        result=zip(n3, result),
        final=zip(n3, result),
        patient=zip(n1, v1),
        split=zip(n2, v2)
        )

@app.route('/RFC')
def RFC():
    cm_dict = {
        'tn' : 1276,
        'fp' : 4,
        'fn' : 123,
        'tp' : 8
    }
   
    accuracy_score = 0.907
    
    # recall: tp / (tp + fn)
    recall  = cm_dict['tp'] / (cm_dict['tp']+ cm_dict['fn'])
    
    # precision tp / (tp + fp)
    precision  = cm_dict['tp'] / (cm_dict['tp'] + cm_dict['fp'])
    
    # f1: 2 tp / (2 tp + fp + fn)
    f1_score  = 2*cm_dict['tp'] / (2*cm_dict['tp'] + cm_dict['fp'] + cm_dict['fn'])
    
    return render_template('RFC.html', accuracy_score = accuracy_score, precision = round(precision,3), recall= round(recall,3), f1_score = round(f1_score,2))

@app.route('/SVC')
def SVC():
    return render_template('SVC.html')

#@app.route('/sequential')
#def sequential():
    #return render_template('sequential.html')

@app.route('/comparison')
def comparison():
    return render_template('comparison.html')


# Create a prediction from app form 
@app.route('/predict', methods=['POST'])
def predict():
    
    if (request.form.get('inlineRadioOptions') == 'RFC'):
        model  = joblib.load('models/bloottest_RFC_selected_features_unscaled.pkl')
       # model  = joblib.load('models/bloottest_RFC_selected_features.pkl')
    elif (request.form.get('inlineRadioOptions') == 'LR'):
        model  = joblib.load('models/bloottest_LR_selected_features_test.pkl')
   # elif (request.form.get('inlineRadioOptions') == 'sequential'):
       # model  = joblib.load('models/tensor_model.pkl')
    elif (request.form.get('inlineRadioOptions') == 'SVC'):
        model  = joblib.load('models/svc_model_covid_blood.pkl')
    else:
        model  = joblib.load('models/bloottest_RFC_selected_features.pkl') 
    
    patient_age_quantile = request.form.get('patient_age_quantile')
    leukocytes = request.form.get('leukocytes')
    platelets = request.form.get('platelets')
    monocytes = request.form.get('monocytes')
    hematocrit = request.form.get('hematocrit')
    eosinophils = request.form.get('eosinophils')
    red_blood_cells = request.form.get('red_blood_cells')
    hemoglobin = request.form.get('hemoglobin')
    lymphocytes = request.form.get('lymphocytes')
    mean_platelet_volume = request.form.get('mean_platelet_volume')
    
    print(request.form.get('inlineRadioOptions')) 
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
                int(patient_age_quantile), 
                float(leukocytes),
                float(platelets),
                float(monocytes),
                float(hematocrit),
                float(eosinophils),
                float(red_blood_cells),
                float(hemoglobin),
                float(lymphocytes),
                float(mean_platelet_volume)
                ]
    #------- use the function if model saved is scaled)------#
    #final_features = scaleInput(features)
    #------- use the function if model saved is scaled)------#
     
    final_features = [np.array(features)]
    prediction = model.predict(final_features)
    predicted_value = prediction[0]
    if int(predicted_value)== 1: 
        prediction_resp ='Positive'
    else: 
        prediction_resp ='Negative'  
                 
    return render_template('index.html', prediction_text=prediction_resp)


#--------------------testing in Postman------------------------------------

# Create a prediction using postman
@app.route('/prediction', methods=['POST'])
def post_prediction():
    patient_age_quantile = request.json['patient_age_quantile']
    leukocytes = request.json['leukocytes']
    platelets = request.json['platelets'] 
    monocytes = request.json['monocytes'] 
    hematocrit = request.json['hematocrit']
    eosinophils = request.json['eosinophils']
    red_blood_cells = request.json['red_blood_cells']
    hemoglobin = request.json['hemoglobin']
    lymphocytes = request.json['lymphocytes'] 
    mean_platelet_volume = request.json['mean_platelet_volume']
    
     
    print(patient_age_quantile, leukocytes)
    print(type(patient_age_quantile), type(leukocytes))

    prediction = Predict(patient_age_quantile, leukocytes, platelets,
            monocytes, hematocrit, eosinophils, red_blood_cells,
            hemoglobin, lymphocytes, mean_platelet_volume)
    
    print(prediction)

    db.session.add(prediction)
    db.session.commit()
    print(predict_schema.jsonify(prediction)) 
    return predict_schema.jsonify(prediction)
    
# verify in postman, get all the predictions
@app.route('/prediction',methods=['GET'])
def get_prodictions():
    predictions = Predict.query.all()
    result = predicts_schema.dump(predictions)
    print(jsonify(result))
    return jsonify(result)

# Get Single Prediction data
@app.route('/prediction/<id>', methods=['GET'])
def get_prodiction(id):
  predict = Predict.query.get(id)
  return predict_schema.jsonify(predict)


# Delete prediction
@app.route('/prediction/<id>', methods=['DELETE'])
def delete_prediction(id):
  predict = Predict.query.get(id)
  db.session.delete(predict)
  db.session.commit()

  return predict_schema.jsonify(predict)
   

# Run Server
if __name__ == '__main__':
    app.run(debug=True)
