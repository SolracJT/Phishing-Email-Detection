from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (accuracy_score, f1_score, recall_score, precision_score)

import pandas as pd
import numpy as np

FILE_PATH: str = 'datasets/phishing_legit_dataset_KD_10000.csv'
LABEL: str = 'label'
RANDOM_STATE: int = 42

df = pd.read_csv(FILE_PATH)

X = df.drop([LABEL])
y = df[LABEL].astype(int)

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=RANDOM_STATE, test_size=0.2, stratify=y)

scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

model_logistics_regression = LogisticRegression()
model_random_forest = RandomForestClassifier()

y_pred = model_logistics_regression.predict(X_test_scaled)
y_proba = model_logistics_regression.predict_proba(X_test_scaled)

print(accuracy_score(y_test, y_pred)
print(precision_score(y_test, y_pred, zero_division=0))
print(recall_score(y_test, y_pred, zero_division=0))
print(f1_score(y_test, y_pred, zero_division=0))