import streamlit as st
import joblib
import os
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import ConfusionMatrixDisplay

# Page configuration
st.set_page_config(
    page_title="Phishing Email Detection",
    page_icon="🛡️",
    layout="wide"
)

# Load trained model
MODEL_PATH = os.path.join("models", "phishing_detector.joblib")

@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH)

model = load_model()

# Example email
EXAMPLE_EMAIL = """URGENT: Your account has been suspended!

Dear Customer,

We detected unusual activity on your account.
Please verify your account immediately by clicking
the link below and confirming your information.

Failure to verify your account within 24 hours
will result in permanent suspension.

Thank you,
Security Department"""

# Session state for email input
if "email_input" not in st.session_state:
    st.session_state.email_input = ""

# Sidebar navigation
st.sidebar.title("🛡️ Phishing Detector")
page = st.sidebar.radio(
    "Navigation",
    ["Email Detector", "Model Evaluation", "About Project"]
)

st.sidebar.divider()
st.sidebar.caption("TF-IDF + Logistic Regression")

# -------------------------
# EMAIL DETECTOR
# -------------------------
if page == "Email Detector":
    st.title("Phishing Email Detection")
    st.write(
        "Analyze email content using a machine learning model "
        "to classify it as Phishing Email or Safe Email."
    )

    st.divider()

    email = st.text_area(
        "Email Content",
        key="email_input",
        height=250,
        placeholder="Paste the email content here..."
    )

    st.caption(f"Characters: {len(email)}")

    col1, col2, col3 = st.columns(3)

    with col1:
        analyze = st.button(
            "🔍 Analyze Email",
            use_container_width=True,
            type="primary"
        )

    with col2:
        if st.button("📝 Load Example", use_container_width=True):
            st.session_state.email_input = EXAMPLE_EMAIL
            st.rerun()

    with col3:
        if st.button("🗑️ Clear", use_container_width=True):
            st.session_state.email_input = ""
            st.rerun()

    if analyze:
        if not email.strip():
            st.warning("Please enter email content first.")
        else:
            prediction = model.predict([email.strip()])[0]

            st.divider()
            st.subheader("Analysis Result")

            if prediction == 1:
                st.error("🚨 Phishing Email")
                st.write(
                    "The model classified this email as a potential "
                    "phishing message. Avoid clicking suspicious links "
                    "or sharing sensitive information."
                )
            else:
                st.success("✅ Safe Email")
                st.write(
                    "The model classified this email as safe. "
                    "However, this result does not guarantee that "
                    "the email is harmless."
                )

            st.info(
                "Model: Logistic Regression | "
                "Feature Extraction: TF-IDF"
            )

# -------------------------
# MODEL EVALUATION
# -------------------------
elif page == "Model Evaluation":
    st.title("Model Evaluation")
    st.write(
        "Performance of the selected model on the held-out test dataset."
    )

    st.divider()

    # Final held-out test metrics
    accuracy = 97.83
    precision = 98.05
    recall = 96.10
    f1_score = 97.07

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Accuracy", f"{accuracy:.2f}%")
    col2.metric("Precision", f"{precision:.2f}%")
    col3.metric("Recall", f"{recall:.2f}%")
    col4.metric("F1-Score", f"{f1_score:.2f}%")

    st.caption(
        "Test set: 3,505 emails | "
        "Training and testing used an 80:20 stratified split."
    )

    st.subheader("Confusion Matrix")

    # Rows: actual labels
    # Columns: predicted labels
    # Label order: Safe Email (0), Phishing Email (1)
    cm = np.array([
        [2171, 25],
        [51, 1258]
    ])

    fig, ax = plt.subplots(figsize=(8, 5))

    disp = ConfusionMatrixDisplay(
        confusion_matrix=cm,
        display_labels=["Safe Email", "Phishing Email"]
    )

    disp.plot(
        ax=ax,
        cmap="Blues",
        values_format="d",
        colorbar=False
    )

    ax.set_title("Final Model Confusion Matrix")
    fig.tight_layout()

    st.pyplot(fig)
    plt.close(fig)

    st.markdown(
        """
        **Interpretation**

        - **2,171 True Negatives:** Safe emails correctly identified.
        - **25 False Positives:** Safe emails incorrectly flagged as phishing.
        - **51 False Negatives:** Phishing emails incorrectly classified as safe.
        - **1,258 True Positives:** Phishing emails correctly detected.
        """
    )

    st.divider()
    st.subheader("Configuration Comparison")

    config1 = {
        "Accuracy": 97.83,
        "Precision": 98.05,
        "Recall": 96.10,
        "F1-Score": 97.07
    }

    config2 = {
        "Accuracy": 94.84,
        "Precision": 98.37,
        "Recall": 87.62,
        "F1-Score": 92.69
    }

    metrics = list(config1.keys())
    values1 = list(config1.values())
    values2 = list(config2.values())

    x = np.arange(len(metrics))
    width = 0.35

    fig2, ax2 = plt.subplots(figsize=(9, 5))

    bars1 = ax2.bar(
        x - width / 2,
        values1,
        width,
        label="Configuration 1"
    )

    bars2 = ax2.bar(
        x + width / 2,
        values2,
        width,
        label="Configuration 2"
    )

    ax2.set_ylabel("Score (%)")
    ax2.set_title("Model Configuration Comparison")
    ax2.set_xticks(x)
    ax2.set_xticklabels(metrics)
    ax2.set_ylim(80, 101)
    ax2.legend()
    ax2.grid(axis="y", linestyle="--", alpha=0.35)

    for bars in (bars1, bars2):
        for bar in bars:
            value = bar.get_height()
            ax2.annotate(
                f"{value:.2f}%",
                (bar.get_x() + bar.get_width() / 2, value),
                xytext=(0, 4),
                textcoords="offset points",
                ha="center",
                fontsize=8
            )

    fig2.tight_layout()
    st.pyplot(fig2)
    plt.close(fig2)

    st.write(
        "**Selected model:** Configuration 1, using word-level "
        "TF-IDF unigram features and Logistic Regression with C=1.0. "
        "It was selected for its stronger overall performance and "
        "higher phishing recall."
    )

# -------------------------
# ABOUT PROJECT
# -------------------------
elif page == "About Project":
    st.title("About the Project")

    st.write(
        "Phishing Email Detection Using TF-IDF and Logistic Regression "
        "is a machine learning project that classifies email text as "
        "Safe Email or Phishing Email."
    )

    st.subheader("Machine Learning Approach")

    col1, col2, col3 = st.columns(3)
    col1.metric("Feature Extraction", "TF-IDF")
    col2.metric("Classifier", "Logistic Regression")
    col3.metric("Classes", "2")

    st.subheader("Dataset Summary")

    col1, col2, col3 = st.columns(3)
    col1.metric("Final Emails", "17,522")
    col2.metric("Safe Emails", "10,978")
    col3.metric("Phishing Emails", "6,544")

    st.subheader("Project Limitations")

    st.write(
        "The model analyzes email text only. It does not independently "
        "verify sender identity, inspect attachments, follow links, "
        "or guarantee that a message classified as safe is harmless. "
        "It should be used as a classification aid rather than a "
        "replacement for comprehensive email security."
    )