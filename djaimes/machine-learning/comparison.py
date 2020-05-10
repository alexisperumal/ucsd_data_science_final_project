import glob as gl
import joblib
import pandas as pd


# Read in models and data
fname = '*.pkl'
path_models = gl.glob(f'../../**/models/{fname}')
fname = 'diagnosis-of-covid-19-and-its-clinical-spectrum.csv'
path = gl.glob(f'../../**//**/{fname}')
df = pd.read_csv(path[0])

# Choose interesting columns and remove missing data
with open('data-columns.txt', 'r') as f:
	colnames = f.read().splitlines()
#df = df[colnames].dropna()
df = df[colnames]
df = df.fillna(df.mean())
print(df['sars_cov_2_exam_result'].value_counts())

# Separate X and y data
category = [0 if result == 'negative' else 1
	for result in df['sars_cov_2_exam_result']]
df['sars_cov_2_exam_result'] = category
X = df.drop('sars_cov_2_exam_result', axis=1)
y = df['sars_cov_2_exam_result'].values.reshape(-1, 1)


fill = list()
# Load in model
for fname in path_models[:3] + [path_models[4]]:
	model = joblib.load(fname)
	predict = model.predict(X)
	fill.append({
		'Model': fname.split('/')[4],
		'Total Positives': predict.sum(),
		'Total Negatives': len(df) - predict.sum()
		})

data = pd.DataFrame(fill)
print(data)
data.to_csv('comparison.csv', index=False)