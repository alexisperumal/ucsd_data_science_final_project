import requests

url = 'http://localhost:5000/predict_api'
#-------------for testing post request---------------------------------#
r = requests.post(url,json={   
                                "patient_age_quantile":  19,
                                "leukocytes": -1.288428,
                                "platelets": -0.906829,
                                "monocytes": 0.567652,
                                "hematocrit": 0.694287,
                                "eosinophils": -0.835508,
                                "red_blood_cells": 0.578024,
                                "hemoglobin": 0.541564,
                                "lymphocytes": -0.295726,
                                "mean_platelet_volume": -0.325903
                                
                            })

print(r.json())