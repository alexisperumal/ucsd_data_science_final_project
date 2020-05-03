import seaborn as sns
from sklearn.metrics import accuracy_score, confusion_matrix, precision_recall_fscore_support
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


def plot_cm(y_test,y_pred,labels):
    # Creates a confusion matrix
    cm = confusion_matrix(y_test, y_pred) # for the tuned model

    # Transform to df for easier plotting
    cm_df = pd.DataFrame(cm,
                        index = labels, 
                        columns = labels)


    plt.figure(figsize=(10,6))  
    sns.heatmap(cm_df, annot=True)
    plt.title('RFC \nAccuracy:{0:.3f}'.format(accuracy_score(y_test, y_pred)))
    plt.ylabel('Actual label')
    plt.xlabel('Predicted label')
    plt.show()