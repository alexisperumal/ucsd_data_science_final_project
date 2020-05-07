import pandas as pd
import matplotlib.pyplot as plt
from mpl_style import greyfox

df = pd.read_csv('random_state_data.csv')

plt.style.use(greyfox)
columns = ['Accuracy', 'Precision', 'Recall']
for c in columns:
	plt.plot(df['random_state'], df[c], '.', label=c)

plt.title('Logistic Regression')
plt.xlabel('Random State Seed')
plt.ylabel('Decimal Number')
lgnd = plt.legend(bbox_to_anchor=(1.02, 1.03))
for i in range(3):
	lgnd.legendHandles[i]._legmarker.set_markersize(26)
plt.tight_layout()
plt.savefig('random_state.png')