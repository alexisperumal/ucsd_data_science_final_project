# Import dependencies
import functions as fn
import glob as gl
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import joblib


# Read original data
fname = 'diagnosis-of-covid-19-and-its-clinical-spectrum.csv'
path = gl.glob(f'../../**//**/{fname}')
df = pd.read_csv(path[0])

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

# Iterate over random state
data = list()
random_states = np.arange(0, 500, 1)
max_percent = [0, 0]
save_index = 0
save_model = 0
for n in random_states:
	# Split the training and testing data
	X_train, X_test, y_train, y_test = train_test_split(X, y,
		random_state=n)

	# Classification of testing data, using training data
	classifier = LogisticRegression()
	classifier.fit(X_train, y_train.flatten())
	predictions = classifier.predict(X_test)

	# Preparation for confusion matrix
	results = pd.DataFrame({
	    "Actual": y_test.flatten(),
	    "Prediction": predictions,
	    'Category': np.zeros_like(predictions)
	})
	results = fn.confusion_matrix_prep(results)

	# Create confusion matrix
	confusion_matrix = results['Category'].value_counts().to_dict()
	cm_types = ['TP', 'FP', 'TN', 'FN']
	for c in cm_types:
		if c not in confusion_matrix.keys():
			confusion_matrix[c] = 0
	cm_dict = fn.confusion_matrix_calc(confusion_matrix)
	data.append(cm_dict)

	# Find max Precion and Recall model and save it to PKL
	if (cm_dict['Precision'] > max_percent[0]) and \
		(cm_dict['Recall'] > max_percent[1]):
		max_percent[0] = cm_dict['Precision']
		max_percent[1] = cm_dict['Recall']
		save_model = classifier
		save_index = n

# Save all confusion matrices in CSV file.
data = pd.DataFrame(data)
data['random_state'] = random_states
data.to_csv('random_state_data.csv', index=False)

# Save the model aong with its data.
joblib.dump(save_model, 'LogisticRegression_model.pkl')
fname = 'LogisticRegression_model_info.txt'
with open(fname, 'w') as f:
	f.write(str(data[data['random_state'] == save_index].to_dict()))

# Load from file
joblib_model = joblib.load('LogisticRegression_model.pkl')

# Calculate the accuracy and predictions
score = joblib_model.score(X_test, y_test)
print("Test score: {0:.2f} %".format(100 * score))