import pandas as pd

fname = 'comparison.csv'
df = pd.read_csv(fname)

# Remove zeros
name = 'Total Positives'
name2 = 'Model'
value = 'bloottest_LR_selected_features_test.pkl'

w = df['Model'] != value

print(df[w][name].sum())

df = df[~w]
w = df[name] != 0

print(df[w])