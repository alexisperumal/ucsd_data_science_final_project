import requests

url = 'http://localhost:5000/predict_api'
# default : 19, -1.288428, -0.906829, 0.567652, 0.694287, -0.835508, 0.578024, 0.541564, -0.295726, -0.325903
r = requests.post(url,json={   "patient_age_quantile":  1.900000e+01,
                                "leukocytes": 6.215833e-09,
                                "platelets": -3.535003e-10,
                                "monocytes": -3.220114e-09,
                                "hematocrit": -2.186214e-09,
                                "eosinophils": 7.206147e-09,
                                "red_blood_cells": 8.424447e-09,
                                "hemoglobin": -1.601319e-08,
                                "lymphocytes": -7.866736e-09,
                                "mean_platelet_volume": 7.438143e-09,
                            })

print(r.json())