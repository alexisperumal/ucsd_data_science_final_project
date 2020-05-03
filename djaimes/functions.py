def confusion_matrix_prep(dataframe):
	dataframe = dataframe.replace(0, 'N')
	dataframe = dataframe.replace(1, 'P')
	for index, row in dataframe.iterrows():
	    if (row['Actual'] == 'N') and (row['Prediction'] == 'N'):
	        cat = 'TN'
	    if (row['Actual'] == 'P') and (row['Prediction'] == 'P'):
	        cat = 'TP'
	    if (row['Actual'] == 'N') and (row['Prediction'] == 'P'):
	        cat = 'FP'
	    if (row['Actual'] == 'P') and (row['Prediction'] == 'N'):
	        cat = 'FN'
	    dataframe['Category'][index] = cat
	return dataframe

def confusion_matrix_calc(dictionary):
	d = dictionary
	population = d['TP'] + d['TN'] + d['FP'] + d['FN']
	accuracy = (d['TP'] + d['TN']) / population
	precision = (d['TP']) / (d['TP'] + d['FP'])
	recall = (d['TP']) / (d['TP'] + d['FN'])
	return {
		'Accuracy': accuracy,
		'Precision': precision,
		'Recall': recall
	}