import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split, StratifiedKFold, cross_validate
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)

import joblib
import os


# ==========================================
# CONFIGURATION
# ==========================================

FILE_PATH = "datasets/Phishing_Email.csv"
RANDOM_STATE = 42


# ==========================================
# LOAD DATA
# ==========================================

df = pd.read_csv(FILE_PATH)

df["Email Text"] = (
    df["Email Text"]
    .fillna("")
    .astype(str)
    .str.strip()
)

# Remove empty emails
df = df[df["Email Text"] != ""]

# Remove duplicate email texts
df = df.drop_duplicates(
    subset=["Email Text"]
).reset_index(drop=True)


# Convert labels
df["label"] = df["Email Type"].map({
    "Safe Email": 0,
    "Phishing Email": 1
})


# ==========================================
# DATASET INFORMATION
# ==========================================

print("==========================================")
print("DATASET INFORMATION")
print("==========================================")

print("Final shape:", df.shape)

print("\nLabels:")
print(df["label"].value_counts())

print("\nDuplicate texts:")
print(df["Email Text"].duplicated().sum())


# ==========================================
# FEATURES AND TARGET
# ==========================================

X = df["Email Text"]
y = df["label"]


# ==========================================
# TRAIN / TEST SPLIT
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=RANDOM_STATE,
    stratify=y
)

print("\n==========================================")
print("TRAIN / TEST SPLIT")
print("==========================================")

print("Training samples:", len(X_train))
print("Testing samples:", len(X_test))


# ==========================================
# CONFIGURATION 1
# Word TF-IDF + Logistic Regression
# ==========================================

config_1 = Pipeline([
    (
        "tfidf",
        TfidfVectorizer(
            lowercase=True,
            stop_words="english",
            ngram_range=(1, 1),
            max_features=10000,
            sublinear_tf=True
        )
    ),
    (
        "model",
        LogisticRegression(
            C=1.0,
            max_iter=1000,
            random_state=RANDOM_STATE
        )
    )
])

# ==========================================
# CONFIGURATION 2: WORD TF-IDF + STRONGER REGULARIZATION
# ==========================================

config_2 = Pipeline([
    ("tfidf", TfidfVectorizer(
        lowercase=True,
        stop_words="english",
        ngram_range=(1, 2),
        max_features=10000,
        sublinear_tf=True
    )),
    ("classifier", LogisticRegression(
        C=0.1,
        max_iter=1000,
        random_state=42
    ))
])


# ==========================================
# CROSS-VALIDATION
# ==========================================

cv = StratifiedKFold(
    n_splits=5,
    shuffle=True,
    random_state=RANDOM_STATE
)


def evaluate_configuration(name, model):

    print("\n==========================================")
    print(name)
    print("==========================================")

    scores = cross_validate(
        model,
        X_train,
        y_train,
        cv=cv,
        scoring=[
            "accuracy",
            "precision",
            "recall",
            "f1"
        ],
        n_jobs=-1
    )

    print("\n5-Fold Cross-Validation:")

    print(
        "Accuracy:",
        scores["test_accuracy"].mean()
    )

    print(
        "Precision:",
        scores["test_precision"].mean()
    )

    print(
        "Recall:",
        scores["test_recall"].mean()
    )

    print(
        "F1:",
        scores["test_f1"].mean()
    )

    # Fit on complete training set
    model.fit(X_train, y_train)

    # Test evaluation
    y_pred = model.predict(X_test)

    print("\nHeld-Out Test Set:")

    accuracy = accuracy_score(
        y_test,
        y_pred
    )

    precision = precision_score(
        y_test,
        y_pred,
        zero_division=0
    )

    recall = recall_score(
        y_test,
        y_pred,
        zero_division=0
    )

    f1 = f1_score(
        y_test,
        y_pred,
        zero_division=0
    )

    print("Accuracy :", accuracy)
    print("Precision:", precision)
    print("Recall   :", recall)
    print("F1 Score :", f1)

    print("\nConfusion Matrix:")

    print(
        confusion_matrix(
            y_test,
            y_pred
        )
    )

    print("\nClassification Report:")

    print(
        classification_report(
            y_test,
            y_pred,
            target_names=[
                "Safe Email",
                "Phishing Email"
            ],
            zero_division=0
        )
    )

    return {
        "model": model,
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1": f1
    }


# ==========================================
# RUN EXPERIMENTS
# ==========================================

result_1 = evaluate_configuration(
    "CONFIGURATION 1: WORD TF-IDF",
    config_1
)

result_2 = evaluate_configuration(
    "CONFIGURATION 2: WORD + CHARACTER TF-IDF",
    config_2
)


# ==========================================
# MODEL COMPARISON
# ==========================================

print("\n==========================================")
print("MODEL COMPARISON")
print("==========================================")

print(
    f"Config 1 F1: {result_1['f1']:.4f}"
)

print(
    f"Config 2 F1: {result_2['f1']:.4f}"
)


if result_2["f1"] > result_1["f1"]:
    best_model = result_2["model"]
    best_name = "Configuration 2"

else:
    best_model = result_1["model"]
    best_name = "Configuration 1"


print("\nSelected model:", best_name)


# ==========================================
# SAVE MODEL
# ==========================================

os.makedirs(
    "models",
    exist_ok=True
)

MODEL_PATH = "models/phishing_detector.joblib"

joblib.dump(
    best_model,
    MODEL_PATH
)

print("\nModel saved to:")
print(MODEL_PATH)