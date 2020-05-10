import glob as gl
import joblib
import pandas as pd

# Read original data
fname = 'diagnosis-of-covid-19-and-its-clinical-spectrum.csv'
path = gl.glob(f'../../**/**/{fname}')
print('\n')
print(f'Data File: {path[0]}')
print('\n')
data = pd.read_csv(path[0])

# Read in model
fname = 'bloottest_RFC_selected_features_unscaled.pkl'
path = gl.glob(f'../../**/models/{fname}')
print(f'Model File: {path[0]}')
print('\n')

# Pick desired columns
with open('data-columns.txt', 'r') as f:
	colnames = f.read().splitlines()
for name in colnames:
	print(name)
print('\n')

# Drop missing values or fill in missing values
data = data[colnames]
data = data.dropna()
#data = data.fillna(data.mean())

# Separate X and y data
category = [0 if result == 'negative' else 1
	for result in data['sars_cov_2_exam_result']]
data['sars_cov_2_exam_result'] = category
X = data.drop('sars_cov_2_exam_result', axis=1)
y = data['sars_cov_2_exam_result'].values.reshape(-1, 1)

# Predict Analysis

model = joblib.load(path[:3])
predict = model.predict(X)
fill = {
	'Model': path[0].split('/')[4],
	'Total Positives': predict.sum(),
	'Total Negatives': len(data) - predict.sum()
	}

print('\n')
data = pd.Series(fill)
print(data)
print('\n')