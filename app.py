import re
import string
import joblib
import streamlit as st
from datetime import datetime


# -------------------------------
# Text Cleaning Function
# -------------------------------
def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"http\S+|www\S+", "", text)
    text = re.sub(r"\d+", "", text)
    text = text.translate(str.maketrans("", "", string.punctuation))
    text = text.strip()
    return text


# -------------------------------
# Spam Keyword Detection
# -------------------------------
def count_spam_keywords(text):
    spam_words = [
        "free", "win", "winner", "cash", "prize", "urgent", "claim",
        "offer", "lottery", "reward", "call", "click", "limited",
        "guaranteed", "congratulations", "bonus", "voucher", "gift",
        "selected", "discount", "deal", "subscribe"
    ]

    text_lower = text.lower()
    found_words = [word for word in spam_words if word in text_lower]
    return found_words


# -------------------------------
# Link Detection
# -------------------------------
def contains_link(text):
    pattern = r"http\S+|www\S+|\.com|\.in|\.org|\.net"
    return bool(re.search(pattern, text.lower()))


# -------------------------------
# Risk Level Function
# -------------------------------
def get_risk_level(spam_confidence):
    if spam_confidence >= 80:
        return "High Risk", "risk-high"
    elif spam_confidence >= 40:
        return "Medium Risk", "risk-medium"
    else:
        return "Low Risk", "risk-low"


# -------------------------------
# Safety Suggestion Function
# -------------------------------
def get_safety_suggestion(prediction, spam_confidence, link_found):
    if prediction == 1:
        if link_found:
            return "This message looks risky. Do not click any links, do not share OTP, and do not call unknown numbers."
        return "This message looks like spam. Avoid replying, calling back, or sharing personal information."
    else:
        if spam_confidence >= 40:
            return "This message seems legitimate, but it has some suspicious signs. Verify the sender before taking action."
        return "This message looks safe, but always be careful with unknown senders."


# -------------------------------
# Load Model and Vectorizer
# -------------------------------
model = joblib.load("models/spam_model.pkl")
vectorizer = joblib.load("models/vectorizer.pkl")


# -------------------------------
# Page Configuration
# -------------------------------
st.set_page_config(
    page_title="Spam SMS Detection",
    page_icon="📩",
    layout="wide"
)


# -------------------------------
# Custom CSS
# -------------------------------
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #111827 45%, #1e1b4b 100%);
        color: white;
    }

    .main-title {
        text-align: center;
        font-size: 46px;
        font-weight: 800;
        color: #ffffff;
        margin-bottom: 5px;
    }

    .sub-title {
        text-align: center;
        font-size: 18px;
        color: #cbd5e1;
        margin-bottom: 35px;
    }

    .small-note {
        color: #cbd5e1;
        font-size: 15px;
        margin-top: -8px;
        margin-bottom: 18px;
    }

    .result-spam {
        background: linear-gradient(135deg, #7f1d1d, #dc2626);
        padding: 26px;
        border-radius: 18px;
        color: white;
        font-size: 26px;
        font-weight: 800;
        text-align: center;
        box-shadow: 0 8px 24px rgba(220, 38, 38, 0.35);
        margin-top: 12px;
        margin-bottom: 18px;
    }

    .result-ham {
        background: linear-gradient(135deg, #064e3b, #10b981);
        padding: 26px;
        border-radius: 18px;
        color: white;
        font-size: 26px;
        font-weight: 800;
        text-align: center;
        box-shadow: 0 8px 24px rgba(16, 185, 129, 0.35);
        margin-top: 12px;
        margin-bottom: 18px;
    }

    .metric-card {
        background: rgba(255, 255, 255, 0.09);
        padding: 22px;
        border-radius: 16px;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.12);
        box-shadow: 0 8px 18px rgba(0, 0, 0, 0.22);
    }

    .metric-value {
        font-size: 30px;
        font-weight: 800;
        color: #38bdf8;
    }

    .metric-label {
        font-size: 14px;
        color: #cbd5e1;
        margin-top: 5px;
    }

    .risk-high {
        background: linear-gradient(135deg, #991b1b, #ef4444);
        padding: 18px;
        border-radius: 15px;
        text-align: center;
        color: white;
        font-size: 22px;
        font-weight: 800;
        box-shadow: 0 8px 20px rgba(239, 68, 68, 0.30);
    }

    .risk-medium {
        background: linear-gradient(135deg, #92400e, #f59e0b);
        padding: 18px;
        border-radius: 15px;
        text-align: center;
        color: white;
        font-size: 22px;
        font-weight: 800;
        box-shadow: 0 8px 20px rgba(245, 158, 11, 0.30);
    }

    .risk-low {
        background: linear-gradient(135deg, #065f46, #10b981);
        padding: 18px;
        border-radius: 15px;
        text-align: center;
        color: white;
        font-size: 22px;
        font-weight: 800;
        box-shadow: 0 8px 20px rgba(16, 185, 129, 0.30);
    }

    .warning-box {
        background: rgba(251, 191, 36, 0.15);
        border-left: 5px solid #fbbf24;
        padding: 16px;
        border-radius: 10px;
        color: #fde68a;
        font-size: 16px;
        margin-top: 8px;
    }

    .safe-box {
        background: rgba(34, 197, 94, 0.15);
        border-left: 5px solid #22c55e;
        padding: 16px;
        border-radius: 10px;
        color: #bbf7d0;
        font-size: 16px;
        margin-top: 8px;
    }

    .suggestion-box {
        background: rgba(59, 130, 246, 0.15);
        border-left: 5px solid #3b82f6;
        padding: 16px;
        border-radius: 10px;
        color: #bfdbfe;
        font-size: 16px;
        margin-top: 8px;
    }

    .history-box {
        background: rgba(255, 255, 255, 0.06);
        padding: 14px;
        border-radius: 12px;
        margin-bottom: 10px;
        border-left: 4px solid #38bdf8;
    }

    .stTextArea textarea {
        border-radius: 15px;
        font-size: 17px;
    }

    .stButton button {
        background: linear-gradient(135deg, #2563eb, #7c3aed);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 10px 24px;
        font-size: 16px;
        font-weight: 700;
        transition: 0.3s;
    }

    .stButton button:hover {
        transform: scale(1.03);
        box-shadow: 0 8px 20px rgba(124, 58, 237, 0.4);
    }

    .stDownloadButton button {
        background: linear-gradient(135deg, #059669, #10b981);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 10px 24px;
        font-size: 16px;
        font-weight: 700;
    }

    hr {
        border: 1px solid rgba(255, 255, 255, 0.12);
        margin-top: 25px;
        margin-bottom: 25px;
    }
</style>
""", unsafe_allow_html=True)


# -------------------------------
# Session State
# -------------------------------
if "history" not in st.session_state:
    st.session_state.history = []

if "sms_text" not in st.session_state:
    st.session_state.sms_text = ""


# -------------------------------
# Example Button Functions
# -------------------------------
def set_spam_example():
    st.session_state.sms_text = "Congratulations! You have won a free cash prize. Call now to claim your reward."


def set_ham_example():
    st.session_state.sms_text = "Hey, are you coming to class tomorrow?"


def set_offer_example():
    st.session_state.sms_text = "Limited time offer! Click now to get free bonus rewards."


def clear_text():
    st.session_state.sms_text = ""


# -------------------------------
# Sidebar
# -------------------------------
with st.sidebar:
    st.title("📌 Project Info")
    st.write("**Project:** Spam SMS Detection")
    st.write("**Technique:** TF-IDF + Machine Learning")
    st.write("**Model:** Naive Bayes / Logistic Regression")
    st.write("**Dataset:** SMS Spam Collection")

    st.divider()

    st.subheader("💡 How it works")
    st.write("1. User enters an SMS")
    st.write("2. Text is cleaned")
    st.write("3. TF-IDF converts text into numbers")
    st.write("4. ML model predicts Spam or Ham")
    st.write("5. Confidence score is displayed")

    st.divider()

    st.subheader("⚠️ Spam Signs")
    st.write("- Free prize")
    st.write("- Urgent call")
    st.write("- Lottery winner")
    st.write("- Suspicious links")
    st.write("- Cash reward")


# -------------------------------
# Header
# -------------------------------
st.markdown("<h1 class='main-title'>📩 Spam SMS Detection</h1>", unsafe_allow_html=True)
st.markdown(
    "<p class='sub-title'>Detect whether an SMS is Spam or Legitimate using Machine Learning</p>",
    unsafe_allow_html=True
)


# -------------------------------
# Example Buttons
# -------------------------------
st.subheader("⚡ Quick Test Examples")
st.markdown(
    "<p class='small-note'>Choose an example message or type your own SMS below.</p>",
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns(3)

with col1:
    st.button("🚨 Spam Example", on_click=set_spam_example, use_container_width=True)

with col2:
    st.button("✅ Ham Example", on_click=set_ham_example, use_container_width=True)

with col3:
    st.button("🎁 Offer Example", on_click=set_offer_example, use_container_width=True)

st.markdown("<hr>", unsafe_allow_html=True)


# -------------------------------
# Input Section
# -------------------------------
st.subheader("✍️ Enter SMS Message")
st.markdown(
    "<p class='small-note'>Type your SMS below, then click Analyze Message.</p>",
    unsafe_allow_html=True
)

user_input = st.text_area(
    "SMS Message",
    key="sms_text",
    height=180,
    placeholder="Example: Congratulations! You have won a free cash prize..."
)

btn_col1, btn_col2, btn_col3 = st.columns([1.2, 1, 5])

with btn_col1:
    predict_button = st.button("🔍 Analyze Message", use_container_width=True)

with btn_col2:
    st.button("🧹 Clear Text", on_click=clear_text, use_container_width=True)

st.markdown("<hr>", unsafe_allow_html=True)


# -------------------------------
# Prediction Section
# -------------------------------
if predict_button:
    if st.session_state.sms_text.strip() == "":
        st.warning("Please enter an SMS message first.")
    else:
        user_message = st.session_state.sms_text

        cleaned_input = clean_text(user_message)
        vectorized_input = vectorizer.transform([cleaned_input])
        prediction = model.predict(vectorized_input)[0]

        if hasattr(model, "predict_proba"):
            probability = model.predict_proba(vectorized_input)[0]
            ham_confidence = probability[0] * 100
            spam_confidence = probability[1] * 100
        else:
            ham_confidence = 0
            spam_confidence = 0

        found_spam_words = count_spam_keywords(user_message)
        link_found = contains_link(user_message)
        risk_level, risk_class = get_risk_level(spam_confidence)
        safety_suggestion = get_safety_suggestion(prediction, spam_confidence, link_found)

        result_text = "Spam" if prediction == 1 else "Ham / Legitimate"

        st.subheader("Prediction Result")

        if prediction == 1:
            st.markdown(
                "<div class='result-spam'>🚨 Result: Spam Message</div>",
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                "<div class='result-ham'>✅ Result: Ham / Legitimate Message</div>",
                unsafe_allow_html=True
            )

        risk_col1, risk_col2 = st.columns([1.3, 2])

        with risk_col1:
            st.markdown(
                f"<div class='{risk_class}'>Risk Level: {risk_level}</div>",
                unsafe_allow_html=True
            )

        with risk_col2:
            st.markdown(
                f"<div class='suggestion-box'>🛡️ <b>Safety Suggestion:</b> {safety_suggestion}</div>",
                unsafe_allow_html=True
            )

        st.markdown("<br>", unsafe_allow_html=True)

        m1, m2, m3, m4 = st.columns(4)

        with m1:
            st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-value'>{spam_confidence:.2f}%</div>
                <div class='metric-label'>Spam Confidence</div>
            </div>
            """, unsafe_allow_html=True)

        with m2:
            st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-value'>{ham_confidence:.2f}%</div>
                <div class='metric-label'>Ham Confidence</div>
            </div>
            """, unsafe_allow_html=True)

        with m3:
            st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-value'>{len(user_message.split())}</div>
                <div class='metric-label'>Total Words</div>
            </div>
            """, unsafe_allow_html=True)

        with m4:
            st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-value'>{len(user_message)}</div>
                <div class='metric-label'>Characters</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        st.subheader("Confidence Analysis")

        st.write("Spam Probability")
        st.progress(int(spam_confidence))

        st.write("Ham Probability")
        st.progress(int(ham_confidence))

        st.subheader("Message Analysis")

        if found_spam_words:
            st.markdown(
                f"<div class='warning-box'>⚠️ Suspicious words found: <b>{', '.join(found_spam_words)}</b></div>",
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                "<div class='safe-box'>✅ No common spam keywords found in this message.</div>",
                unsafe_allow_html=True
            )

        if link_found:
            st.markdown(
                "<div class='warning-box'>🔗 This message contains a link or website pattern. Be careful before clicking.</div>",
                unsafe_allow_html=True
            )

        with st.expander("View cleaned text used by the model"):
            st.write(cleaned_input)

        # -------------------------------
        # Download Report
        # -------------------------------
        report = f"""
Spam SMS Detection Report
=========================

Date and Time:
{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

Original Message:
{user_message}

Cleaned Message:
{cleaned_input}

Prediction:
{result_text}

Risk Level:
{risk_level}

Spam Confidence:
{spam_confidence:.2f}%

Ham Confidence:
{ham_confidence:.2f}%

Total Words:
{len(user_message.split())}

Total Characters:
{len(user_message)}

Suspicious Keywords:
{", ".join(found_spam_words) if found_spam_words else "None"}

Link Detected:
{"Yes" if link_found else "No"}

Safety Suggestion:
{safety_suggestion}
"""

        st.download_button(
            label="📄 Download Prediction Report",
            data=report,
            file_name="spam_sms_prediction_report.txt",
            mime="text/plain"
        )

        # Save History
        st.session_state.history.append({
            "time": datetime.now().strftime("%H:%M:%S"),
            "message": user_message,
            "result": result_text,
            "risk_level": risk_level,
            "spam_confidence": f"{spam_confidence:.2f}%"
        })


# -------------------------------
# Prediction History
# -------------------------------
if st.session_state.history:
    st.markdown("<hr>", unsafe_allow_html=True)
    st.subheader("Prediction History")

    for item in reversed(st.session_state.history[-5:]):
        st.markdown(f"""
        <div class='history-box'>
            <b>{item['time']}</b> | 
            <b>{item['result']}</b> | 
            Risk: <b>{item['risk_level']}</b> | 
            Spam Confidence: <b>{item['spam_confidence']}</b>
            <br>
            <span style='color:#cbd5e1;'>{item['message']}</span>
        </div>
        """, unsafe_allow_html=True)

    if st.button("Clear History"):
        st.session_state.history = []
        st.rerun()


# -------------------------------
# Footer
# -------------------------------
st.markdown("""
<br>
<center>
    <p style='color:#94a3b8;'>
        Built with Python, Streamlit, TF-IDF and Machine Learning
    </p>
</center>
""", unsafe_allow_html=True)