# Import dependencies
import glob as gl
import numpy as np
import pandas as pd


# Read original data
fname = 'diagnosis-of-covid-19-and-its-clinical-spectrum.csv'
path = gl.glob(f'../**//**/{fname}')
df = pd.read_csv(path[0])
nrows, ncols = df.shape
data = {'original': {'nrows': nrows, 'ncols': ncols}}

# Choose interesting columns and remove missing data
with open('data-columns.txt', 'r') as f:
	colnames = f.read().splitlines()
df = df[colnames].dropna()

# Separate X and y data
category = [0 if result == 'negative' else 1
	for result in df['sars_cov_2_exam_result']]
df['sars_cov_2_exam_result'] = category
X = df.drop('sars_cov_2_exam_result', axis=1)
y = df['sars_cov_2_exam_result'].values.reshape(-1, 1)

print(X.shape, y.shape)