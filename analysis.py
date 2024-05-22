import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from xgboost import XGBClassifier
from sklearn import metrics

df = pd.read_csv("btc15m.csv")

features = ["open", "high", "low", "close", "volume"]

plt.subplots(figsize=(20, 10))

for i, col in enumerate(features):

    plt.subplot(2, 3, i + 1)

    sb.distplot(df[col])
plt.show()
