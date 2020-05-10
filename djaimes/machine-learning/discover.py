import glob as gl
import numpy as np
import pandas as pd


# Read original data
fname = 'diagnosis-of-covid-19-and-its-clinical-spectrum.csv'
path = gl.glob(f'../../**//**/{fname}')
df = pd.read_csv(path[0])

# Choose interesting columns and remove missing data
with open('data-columns.txt', 'r') as f:
	colnames = f.read().splitlines()
df = df[colnames].dropna()
df = df.reset_index(drop=True)

print(df[df['sars_cov_2_exam_result'] == 'positive'].iloc[8])

# Total Patients
print(f'Total patients: {len(df)}')
neg = sum(df['sars_cov_2_exam_result'] == 'negative')
print(f'Negative patients: {neg}')
print(f'Positive patients: {len(df) - neg}')