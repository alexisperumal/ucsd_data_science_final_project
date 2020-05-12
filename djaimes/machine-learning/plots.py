import pandas as pd
import matplotlib.pyplot as plt
import functions as fn


LR_cm = {
	'TN': 128,
	'FP': 3,
	'FN': 7,
	'TP': 12
}

RFC_cm = {
	'TN': 1276,
	'FP': 4,
	'FN': 123,
	'TP': 8
}

SVC_cm = {
	'TN': 1270,
	'FP': 3,
	'FN': 131,
	'TP': 7
}

df = pd.DataFrame({
	'LR': fn.confusion_matrix_calc(LR_cm),
	'RFC': fn.confusion_matrix_calc(RFC_cm),
	'SVC': fn.confusion_matrix_calc(SVC_cm),
	})



plt.figure(figsize=(14, 8))
plt.style.use('ggplot')
df.plot(kind='barh')

for i, (index, row) in enumerate(df.iterrows()):
    plt.text(row['LR'] + 0.22, i - 0.08,
        f"{round(100 * row['LR'], 1):<04}%",
        va='top', ha='right', fontsize=18, color='C0')
    plt.text(row['RFC'] + 0.22, i + 0.07,
        f"{round(100 * row['RFC'], 1):<04}%",
        va='top', ha='right', fontsize=18, color='C1')
    plt.text(row['SVC'] + 0.22, i + 0.24,
        f"{round(100 * row['SVC'], 1):<04}%",
        va='top', ha='right', fontsize=18, color='C2')

plt.xlim(0, 1.2)
plt.gca().set_yticklabels(df.index, fontsize=18)
plt.xticks([])
plt.grid()

plt.tight_layout()
plt.savefig('comparison.png', dpi=300)