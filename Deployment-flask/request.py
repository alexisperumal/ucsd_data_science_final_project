import requests

url = 'http://127.0.0.1:5000/predict_api'
r = requests.post(url,json={'patient age quantile':17, 
                            'leukocytes':-0.094610348, 
                            'platelets':-0.51741302,
                            'monocytes':0.357546657,
                            'hematocrit':-1.571682215,
                            'red_blood_cells':-0.850035012,
                            'lymphocytes':0.318365753,
                            'eosinophils':1.482158184,
                            'hemoglobin':-0.774212003,
                            })

print(r.json())