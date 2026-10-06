from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score

from sklearn.metrics import (
accuracy_score, precision_score, recall_score,
    f1_score, confusion_matrix, classification_report)

from sklearn.pipeline import Pipeline

import pandas as pd

FILE_PATH: str = "datasets/phishing_legit_dataset_KD_10000.csv"
TEXT_COLUMN: str = "text"
LABEL_COLUMN: str = "label"

RANDOM_STATE: int = 42
TEST_SIZE: float = 0.20
CV_FOLDS: int = 5

# ==========================================
# LOAD DATASET
# ==========================================

df = pd.read_csv(FILE_PATH)

print("Dataset shape:", df.shape)

print("\nLabel distribution:")
print(df[LABEL_COLUMN].value_counts())


# ==========================================
# SELECT FEATURES AND TARGET
# ==========================================

X = df[TEXT_COLUMN].fillna("")
y = df[LABEL_COLUMN].astype(int)

# ==========================================
# TRAIN / TEST SPLIT
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=TEST_SIZE,
    random_state=RANDOM_STATE,
    stratify=y
)

# ==========================================
# TF-IDF CONFIGURATION
# ==========================================

tfidf = TfidfVectorizer(
    lowercase=True,
    stop_words="english",
    max_features=5000,
    ngram_range=(1, 1)
)

# ==========================================
# CONFIGURATION 1
# Logistic Regression C = 1.0
# ==========================================

model_config_1 = Pipeline([
    ("tfidf", tfidf),
    ("model", LogisticRegression(
        C=1.0,
        max_iter=1000,
        random_state=RANDOM_STATE
    ))
])

# ==========================================
# CONFIGURATION 2
# Logistic Regression C = 0.1
# Stronger regularization
# ==========================================

model_config_2 = Pipeline([
    ("tfidf", TfidfVectorizer(
        lowercase=True,
        stop_words="english",
        max_features=5000,
        ngram_range=(1, 1)
    )),
    ("model", LogisticRegression(
        C=0.1,
        max_iter=1000,
        random_state=RANDOM_STATE
    ))
])

# ==========================================
# 5-FOLD CROSS-VALIDATION
# ==========================================

cv = StratifiedKFold(
    n_splits=CV_FOLDS,
    shuffle=True,
    random_state=RANDOM_STATE
)

print("\n========================================")
print("CROSS-VALIDATION")
print("========================================")

cv_scores_config_1 = cross_val_score(
    model_config_1,
    X_train,
    y_train,
    cv=cv,
    scoring="f1"
)

cv_scores_config_2 = cross_val_score(
    model_config_2,
    X_train,
    y_train,
    cv=cv,
    scoring="f1"
)

print("\nConfiguration 1")
print("C = 1.0")
print("F1 scores:", cv_scores_config_1)
print("Mean F1:", cv_scores_config_1.mean())

print("\nConfiguration 2")
print("C = 0.1")
print("F1 scores:", cv_scores_config_2)
print("Mean F1:", cv_scores_config_2.mean())

# ==========================================
# TRAIN CONFIGURATION 1
# ==========================================

model_config_1.fit(X_train, y_train)

y_pred_1 = model_config_1.predict(X_test)

# ==========================================
# TRAIN CONFIGURATION 2
# ==========================================

model_config_2.fit(X_train, y_train)

y_pred_2 = model_config_2.predict(X_test)

# ==========================================
# EVALUATION FUNCTION
# ==========================================

def evaluate_model(name, y_test, y_pred):
    print("\n========================================")
    print(name)
    print("========================================")

    accuracy = accuracy_score(y_test, y_pred)
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

    print("\nClassification Report:")
    print(
        classification_report(
            y_test,
            y_pred,
            target_names=["Legitimate", "Phishing"],
            zero_division=0
        )
    )

    print("Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))

    return {
        "Configuration": name,
        "Accuracy": accuracy,
        "Precision": precision,
        "Recall": recall,
        "F1 Score": f1
    }

# ==========================================
# EVALUATE BOTH CONFIGURATIONS
# ==========================================

result_1 = evaluate_model(
    "Configuration 1: C = 1.0",
    y_test,
    y_pred_1
)

result_2 = evaluate_model(
    "Configuration 2: C = 0.1",
    y_test,
    y_pred_2
)

# ==========================================
# COMPARISON TABLE
# ==========================================

results = pd.DataFrame([
    result_1,
    result_2
])

print("\n========================================")
print("MODEL COMPARISON")
print("========================================")

print(results.to_string(index=False))

# ==========================================
# SELECT BEST CONFIGURATION
# ==========================================

best_configuration = results.loc[
    results["F1 Score"].idxmax()
]

print("\n========================================")
print("BEST CONFIGURATION")
print("========================================")

print(best_configuration)