import os
import joblib
import streamlit as st
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# =====================================================
# PAGE CONFIGURATION
# =====================================================
st.set_page_config(
    page_title="Phishing Email Detection",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# PROJECT SETTINGS
# =====================================================
MODEL_PATH = os.path.join("models", "phishing_detector.joblib")

GITHUB_URL = "https://github.com/SolracJT/Phishing-Email-Detection"
DOCS_URL = "https://docs.google.com/document/d/158QBPo9VJkvhNE59U4q9saSwNBXCTlEQ/edit"

TOTAL_EMAILS = 17522
SAFE_EMAILS = 10978
PHISHING_EMAILS = 6544

ACCURACY = 97.83
PRECISION = 98.05
RECALL = 96.10
F1_SCORE = 97.07

# Chart colors
NAVY = "#172554"
BLUE = "#3B82F6"
CYAN = "#06B6D4"
GREEN = "#16A34A"
RED = "#DC2626"
MUTED = "#64748B"
GRID = "#E2E8F0"

# =====================================================
# LOAD MODEL
# =====================================================
@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH)

model = load_model()

# =====================================================
# SESSION STATE
# =====================================================
EXAMPLE_EMAIL = """URGENT: Your account has been suspended!

Dear Customer,

We detected unusual activity on your account.
Please verify your account immediately by clicking
the link below and confirming your information.

Failure to verify your account within 24 hours
will result in permanent suspension.

Thank you,
Security Department"""

if "email_input" not in st.session_state:
    st.session_state.email_input = ""

def load_example():
    st.session_state.email_input = EXAMPLE_EMAIL

def clear_email():
    st.session_state.email_input = ""

# =====================================================
# CUSTOM STYLE
# =====================================================
st.markdown("""
<style>
    .stApp {
        background-color: #F8FAFC;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1450px;
    }

    [data-testid="stSidebar"] {
        background-color: #F1F5F9;
        border-right: 1px solid #E2E8F0;
    }

    .hero {
        background: linear-gradient(120deg, #172554 0%, #1D4ED8 100%);
        padding: 28px 30px;
        border-radius: 18px;
        color: white;
        margin: 10px 0 24px 0;
    }

    .hero h2 {
        color: white;
        margin: 0 0 8px 0;
        font-size: 28px;
    }

    .hero p {
        color: #DBEAFE;
        margin: 0;
        font-size: 15px;
        line-height: 1.6;
    }

    .section-note {
        color: #64748B;
        font-size: 14px;
        margin-top: -8px;
        margin-bottom: 18px;
    }

    div[data-testid="stMetric"] {
        background-color: white;
        border: 1px solid #E2E8F0;
        padding: 18px 20px;
        border-radius: 14px;
        box-shadow: 0 2px 8px rgba(15, 23, 42, 0.035);
    }

    div[data-testid="stMetricLabel"] {
        color: #64748B;
    }

    div[data-testid="stMetricValue"] {
        color: #172554;
        font-weight: 700;
    }

    div.stButton > button,
    div.stLinkButton > a {
        border-radius: 10px;
        font-weight: 600;
    }

    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 14px;
    }

    hr {
        border-color: #E2E8F0;
    }
</style>
""", unsafe_allow_html=True)

# =====================================================
# PLOTLY THEME HELPER
# =====================================================
def style_chart(fig, height=380):
    fig.update_layout(
        template="plotly_white",
        height=height,
        margin=dict(l=20, r=20, t=65, b=25),
        font=dict(
            family="Arial, sans-serif",
            size=13,
            color=NAVY
        ),
        title=dict(
            x=0.02,
            xanchor="left",
            font=dict(size=17, color=NAVY)
        ),
        paper_bgcolor="white",
        plot_bgcolor="white",
        legend=dict(
            bgcolor="rgba(255,255,255,0)",
            borderwidth=0
        ),
        hoverlabel=dict(
            bgcolor=NAVY,
            font_size=13,
            font_color="white"
        )
    )

    fig.update_xaxes(
        showgrid=True,
        gridcolor=GRID,
        zeroline=False
    )

    fig.update_yaxes(
        showgrid=False,
        zeroline=False
    )

    return fig

# =====================================================
# SIDEBAR
# =====================================================
with st.sidebar:
    st.markdown("## 🛡️ Phishing Detector")
    st.caption("Machine Learning Research Project")
    st.divider()

    page = st.radio(
        "NAVIGATION",
        [
            "Email Detector",
            "Dataset Overview",
            "Model Evaluation",
            "About Project"
        ],
        label_visibility="visible"
    )

    st.divider()
    st.markdown("### Research Resources")

    st.link_button(
        "📂 GitHub Repository",
        GITHUB_URL,
        use_container_width=True
    )

    if DOCS_URL.startswith("https://"):
        st.link_button(
            "📄 Research Document",
            DOCS_URL,
            use_container_width=True
        )
    else:
        st.caption(
            "Add your Google Docs URL to DOCS_URL in app.py."
        )

    st.divider()
    st.caption("TF-IDF + Logistic Regression")
    st.caption("Binary email classification")

# =====================================================
# EMAIL DETECTOR
# =====================================================
if page == "Email Detector":

    st.markdown("""
    <div class="hero">
        <h2>Email Security Analysis</h2>
        <p>
            Analyze email content using TF-IDF and Logistic Regression.
            Identify potentially suspicious messages in seconds.
        </p>
    </div>
    """, unsafe_allow_html=True)

    left, right = st.columns([1.65, 1], gap="large")

    with left:
        st.subheader("Email Content")
        st.markdown(
            '<p class="section-note">Paste the email message you want to analyze.</p>',
            unsafe_allow_html=True
        )

        email = st.text_area(
            "Email message",
            key="email_input",
            height=280,
            placeholder=(
                "Paste the email subject and body here...\n\n"
                "Example: Dear Customer, we noticed unusual activity..."
            ),
            label_visibility="collapsed"
        )

        st.caption(f"{len(email):,} characters")

        btn1, btn2, btn3 = st.columns(3)

        with btn1:
            analyze = st.button(
                "🔍 Analyze Email",
                type="primary",
                use_container_width=True
            )

        with btn2:
            st.button(
                "📝 Load Example",
                on_click=load_example,
                use_container_width=True
            )

        with btn3:
            st.button(
                "Clear",
                on_click=clear_email,
                use_container_width=True
            )

    with right:
        st.subheader("Detection Method")

        with st.container(border=True):
            st.markdown("#### 01 · Feature Extraction")
            st.write("TF-IDF converts email text into numerical features.")

            st.divider()

            st.markdown("#### 02 · Classification")
            st.write("Logistic Regression predicts one of two email classes.")

            st.divider()

            st.markdown("#### 03 · Result")
            st.markdown(
                f"**Model accuracy:** {ACCURACY:.2f}%"
            )
            st.caption(
                "Measured on the held-out test dataset. "
                "This is not a guarantee for individual emails."
            )

    if analyze:
        if not email.strip():
            st.warning("Please enter email content before analyzing.")
        else:
            prediction = model.predict([email.strip()])[0]

            st.divider()
            st.subheader("Analysis Result")

            if prediction == 1:
                st.error("🚨 Phishing Email")
                st.write(
                    "The model classified this message as potentially "
                    "phishing. Avoid interacting with suspicious links "
                    "or sharing sensitive information."
                )
            else:
                st.success("✅ Safe Email")
                st.write(
                    "The model classified this message as safe. "
                    "This does not guarantee that the email is harmless."
                )

            result_col1, result_col2 = st.columns(2)

            with result_col1:
                st.metric(
                    "Predicted Class",
                    "Phishing Email" if prediction == 1 else "Safe Email"
                )

            with result_col2:
                st.metric("Classification Method", "TF-IDF + LR")

            st.caption(
                "Text-based classification only. Sender identity, "
                "attachments, and linked websites are not independently "
                "verified."
            )

# =====================================================
# DATASET OVERVIEW
# =====================================================
elif page == "Dataset Overview":

    st.title("Dataset Overview")
    st.markdown(
        '<p class="section-note">Composition of the cleaned email dataset used in this project.</p>',
        unsafe_allow_html=True
    )

    safe_pct = SAFE_EMAILS / TOTAL_EMAILS * 100
    phishing_pct = PHISHING_EMAILS / TOTAL_EMAILS * 100

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Emails", f"{TOTAL_EMAILS:,}")
    col2.metric("Safe Emails", f"{SAFE_EMAILS:,}", f"{safe_pct:.2f}% of dataset")
    col3.metric("Phishing Emails", f"{PHISHING_EMAILS:,}", f"{phishing_pct:.2f}% of dataset")

    st.divider()
    st.subheader("Class Distribution")

    chart_left, chart_right = st.columns(2, gap="large")

    # Donut chart
    with chart_left:
        donut = go.Figure(
            data=[
                go.Pie(
                    labels=["Safe Email", "Phishing Email"],
                    values=[SAFE_EMAILS, PHISHING_EMAILS],
                    hole=0.68,
                    sort=False,
                    marker=dict(
                        colors=[GREEN, RED],
                        line=dict(color="white", width=4)
                    ),
                    textinfo="percent",
                    textposition="outside",
                    hovertemplate=(
                        "<b>%{label}</b><br>"
                        "Emails: %{value:,}<br>"
                        "Share: %{percent}<extra></extra>"
                    )
                )
            ]
        )

        donut.update_layout(
            title="Dataset Composition",
            annotations=[
                dict(
                    text=f"<b>{TOTAL_EMAILS:,}</b><br><sup>Total emails</sup>",
                    x=0.5,
                    y=0.5,
                    font=dict(size=19, color=NAVY),
                    showarrow=False
                )
            ],
            showlegend=True,
            legend=dict(orientation="h", y=-0.12, x=0.5, xanchor="center")
        )

        style_chart(donut, 420)
        st.plotly_chart(donut, use_container_width=True)

    # Horizontal bar chart
    with chart_right:
        bar = px.bar(
            x=[SAFE_EMAILS, PHISHING_EMAILS],
            y=["Safe Email", "Phishing Email"],
            orientation="h",
            text=[f"{SAFE_EMAILS:,}", f"{PHISHING_EMAILS:,}"],
            color=["Safe Email", "Phishing Email"],
            color_discrete_map={
                "Safe Email": GREEN,
                "Phishing Email": RED
            },
            labels={
                "x": "Number of Emails",
                "y": "Class",
                "color": "Email Class"
            },
            title="Email Count by Class"
        )

        bar.update_traces(
            textposition="outside",
            cliponaxis=False,
            hovertemplate="%{y}<br>Emails: %{x:,}<extra></extra>"
        )

        bar.update_layout(
            showlegend=False,
            xaxis=dict(range=[0, SAFE_EMAILS * 1.22])
        )

        style_chart(bar, 420)
        st.plotly_chart(bar, use_container_width=True)

    st.divider()
    st.subheader("Dataset Details")

    info1, info2 = st.columns(2)

    with info1:
        with st.container(border=True):
            st.markdown("#### Dataset Information")
            st.write("**Source:** Phishing Email Dataset on Kaggle")
            st.write("**Original records:** 18,650")
            st.write("**Final cleaned records:** 17,522")
            st.write("**Train-test split:** 80:20, stratified")
            st.write("**Missing values:** 0")

    with info2:
        with st.container(border=True):
            st.markdown("#### Classification Labels")
            st.write("**Input feature:** `Email Text`")
            st.write("**Target label:** `Email Type`")
            st.write("**Label 0:** Safe Email")
            st.write("**Label 1:** Phishing Email")

    st.info(
        "The final dataset contains 10,978 safe emails and 6,544 phishing "
        "emails after duplicate email texts were removed."
    )

# =====================================================
# MODEL EVALUATION
# =====================================================
elif page == "Model Evaluation":

    st.title("Model Evaluation")
    st.markdown(
        '<p class="section-note">Held-out test performance and comparison of the two model configurations.</p>',
        unsafe_allow_html=True
    )

    m1, m2, m3, m4 = st.columns(4)

    m1.metric("Accuracy", f"{ACCURACY:.2f}%")
    m2.metric("Precision", f"{PRECISION:.2f}%")
    m3.metric("Recall", f"{RECALL:.2f}%")
    m4.metric("F1-Score", f"{F1_SCORE:.2f}%")

    st.caption("Evaluation set: 3,505 emails · Stratified 80:20 split")

    st.divider()
    st.subheader("Confusion Matrix")

    cm = np.array([
        [2171, 25],
        [51, 1258]
    ])

    labels = ["Safe Email", "Phishing Email"]

    heatmap = go.Figure(
        data=go.Heatmap(
            z=cm,
            x=labels,
            y=labels,
            colorscale=[
                [0.0, "#EFF6FF"],
                [0.5, "#60A5FA"],
                [1.0, "#1D4ED8"]
            ],
            showscale=False,
            text=cm,
            texttemplate="%{text:,}",
            textfont=dict(size=22, color=NAVY),
            hovertemplate=(
                "Actual: %{y}<br>"
                "Predicted: %{x}<br>"
                "Count: %{z:,}<extra></extra>"
            )
        )
    )

    heatmap.update_layout(
        title="Actual vs. Predicted Class",
        xaxis_title="Predicted Label",
        yaxis_title="Actual Label",
        yaxis=dict(autorange="reversed", scaleanchor="x"),
    )

    style_chart(heatmap, 430)
    st.plotly_chart(heatmap, use_container_width=True)

    with st.expander("Interpret the confusion matrix"):
        cm1, cm2, cm3, cm4 = st.columns(4)
        cm1.metric("True Negatives", "2,171")
        cm2.metric("False Positives", "25")
        cm3.metric("False Negatives", "51")
        cm4.metric("True Positives", "1,258")

        st.write(
            "False negatives are phishing emails incorrectly classified "
            "as safe. There were 51 false negatives in the test set."
        )

    st.divider()
    st.subheader("Configuration Comparison")

    metrics = ["Accuracy", "Precision", "Recall", "F1-Score"]
    config1 = [97.83, 98.05, 96.10, 97.07]
    config2 = [94.84, 98.37, 87.62, 92.69]

    comparison = go.Figure()

    comparison.add_trace(
        go.Bar(
            name="Configuration 1",
            x=metrics,
            y=config1,
            marker_color=BLUE,
            text=[f"{v:.2f}%" for v in config1],
            textposition="outside",
            cliponaxis=False,
            hovertemplate="%{x}<br>Score: %{y:.2f}%<extra></extra>"
        )
    )

    comparison.add_trace(
        go.Bar(
            name="Configuration 2",
            x=metrics,
            y=config2,
            marker_color=CYAN,
            text=[f"{v:.2f}%" for v in config2],
            textposition="outside",
            cliponaxis=False,
            hovertemplate="%{x}<br>Score: %{y:.2f}%<extra></extra>"
        )
    )

    comparison.update_layout(
        title="Model Performance by Metric",
        barmode="group",
        yaxis=dict(
            title="Score (%)",
            range=[80, 102],
            ticksuffix="%"
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )

    style_chart(comparison, 450)
    st.plotly_chart(comparison, use_container_width=True)

    st.success(
        "Configuration 1 was selected for its stronger overall "
        "performance and higher phishing recall."
    )

    st.caption(
        "Configuration 1: unigram TF-IDF, C=1.0. "
        "Configuration 2: unigram and bigram TF-IDF, C=0.1."
    )

# =====================================================
# ABOUT PROJECT
# =====================================================
elif page == "About Project":

    st.markdown("""
    <div class="hero">
        <h2>About the Project</h2>
        <p>
            Phishing Email Detection Using TF-IDF and Logistic Regression.
            A machine learning web application that classifies email text
            into safe and phishing categories.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("How It Works")

    c1, c2, c3 = st.columns(3)

    with c1:
        with st.container(border=True):
            st.markdown("### 01")
            st.markdown("#### Email Input")
            st.write("The user provides the text of an email.")

    with c2:
        with st.container(border=True):
            st.markdown("### 02")
            st.markdown("#### TF-IDF")
            st.write("Email text is converted into numerical features.")

    with c3:
        with st.container(border=True):
            st.markdown("### 03")
            st.markdown("#### Classification")
            st.write("Logistic Regression predicts the email class.")

    st.divider()
    st.subheader("Technology Stack")

    t1, t2, t3, t4 = st.columns(4)
    t1.metric("Classifier", "Logistic Regression")
    t2.metric("Feature Extraction", "TF-IDF")
    t3.metric("Max Features", "10,000")
    t4.metric("Classes", "2")

    st.divider()
    st.subheader("Research Resources")

    r1, r2 = st.columns(2)

    with r1:
        with st.container(border=True):
            st.markdown("#### 💻 Source Code")
            st.write("Explore the project code and implementation.")
            st.link_button(
                "Open GitHub Repository",
                GITHUB_URL,
                use_container_width=True
            )

    with r2:
        with st.container(border=True):
            st.markdown("#### 📚 Research Documentation")
            st.write("Read the project's documentation and methodology.")

            if DOCS_URL.startswith("https://"):
                st.link_button(
                    "Open Google Docs",
                    DOCS_URL,
                    use_container_width=True
                )
            else:
                st.warning("Configure your Google Docs URL in app.py.")

    st.divider()
    st.subheader("Scope and Limitations")

    st.write(
        "The classifier analyzes email text only. It does not independently "
        "verify sender identity, inspect attachments, or access linked "
        "websites. A safe prediction does not guarantee that an email is "
        "harmless. The application is intended as a classification aid."
    )