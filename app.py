import streamlit as st
import joblib
import os

# Page configuration
st.set_page_config(
    page_title="Phishing Email Detection",
    page_icon="🛡️",
    layout="centered"
)

# Load trained model
MODEL_PATH = os.path.join("models", "phishing_detector.joblib")
model = joblib.load(MODEL_PATH)

# Header
st.title("Phishing Email Detection")
st.write(
    "Enter an email message below to classify it as "
    "Phishing Email or Safe Email using TF-IDF and Logistic Regression."
)

st.divider()

# Email input
email = st.text_area(
    "Email Content",
    height=250,
    placeholder="Paste the email content here..."
)

# Character count
st.caption(f"Characters: {len(email)}")

# Buttons
col1, col2 = st.columns(2)

with col1:
    analyze = st.button(
        "Analyze Email",
        use_container_width=True
    )

with col2:
    example = st.button(
        "Load Example",
        use_container_width=True
    )

# Example email
if example:
    email = """URGENT: Your account has been suspended!

Dear Customer,

We detected unusual activity on your account.
Please verify your account immediately by clicking
the link below and confirming your information.

Failure to verify your account within 24 hours
will result in permanent suspension.

Thank you,
Security Department"""

    st.text_area(
        "Example Email",
        value=email,
        height=250
    )

# Prediction
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
                "The model classified this email as a phishing message."
            )
        else:
            st.success("✅ Safe Email")
            st.write(
                "The model classified this email as a safe message."
            )

        st.info(
            "Model: Logistic Regression  |  "
            "Feature Extraction: TF-IDF"
        )