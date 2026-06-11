import streamlit as st
import datetime
import requests
import os
from dotenv import load_dotenv
from main import fetch_news, analyze_articles

# Load API key
load_dotenv()
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

st.set_page_config(
    page_title="AI News Intelligence Dashboard",
    page_icon="🧠",
    layout="wide"
)

# ----------------------------
# Custom Background + UI
# ----------------------------
st.markdown("""
<style>

.stApp {
background: linear-gradient(135deg,#0f172a,#020617);
color:white;
}

.title {
font-size:42px;
font-weight:700;
text-align:center;
background:linear-gradient(90deg,#06b6d4,#22c55e);
-webkit-background-clip:text;
-webkit-text-fill-color:transparent;
}

.subtitle{
text-align:center;
color:#9ca3af;
margin-bottom:30px;
}

.card {
background: rgba(255,255,255,0.05);
padding:25px;
border-radius:14px;
margin-bottom:25px;
border:1px solid rgba(255,255,255,0.08);
box-shadow:0 8px 25px rgba(0,0,0,0.6);
}

.badge {
padding:6px 12px;
border-radius:20px;
font-size:13px;
margin-right:8px;
color:white;
font-weight:500;
}

.footer{
text-align:center;
margin-top:40px;
color:#9ca3af;
font-size:14px;
}

</style>
""", unsafe_allow_html=True)

# ----------------------------
# Header
# ----------------------------
st.markdown('<div class="title">📰 Real-Time News Intelligence using Generative AI</div>', unsafe_allow_html=True)

st.markdown("""
<div class="subtitle">
AI-powered pipeline for real-time news retrieval, summarization, sentiment analysis and impact detection
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ----------------------------
# Sidebar
# ----------------------------
st.sidebar.header("⚙ Control Panel")

category = st.sidebar.selectbox(
"Select News Category",
["business","entertainment","health","science","sports","technology"]
)

st.sidebar.markdown("---")

st.sidebar.markdown("### 🤖 AI Model")

st.sidebar.markdown("""
FLAN-T5 Transformer

Capabilities

• News Summarization  
• Sentiment Analysis  
• Impact Detection  
""")

# ----------------------------
# Fetch Headlines
# ----------------------------
def fetch_headlines(category):

    url = f"https://newsapi.org/v2/top-headlines?country=us&category={category}&pageSize=5&apiKey={NEWS_API_KEY}"

    response = requests.get(url)
    data = response.json()

    return data.get("articles", [])

# ----------------------------
# Generate AI Insights
# ----------------------------
if st.button("🚀 Generate AI Insights"):

    with st.spinner("Analyzing global news with AI..."):

        articles = fetch_news(category)
        results = analyze_articles(articles)

        headlines = fetch_headlines(category)

    st.success("AI Intelligence Report Generated")
    st.caption(f"Generated at {datetime.datetime.now()}")

    st.markdown("## 📰 Top Headlines")

    for news in headlines:
        st.write("•", news["title"])

    st.markdown("---")

    st.markdown("## 🧠 AI Generated Insights")

    sentiment_color = {
    "Positive":"#22c55e",
    "Neutral":"#f59e0b",
    "Negative":"#ef4444"
    }

    impact_color = {
    "High":"#06b6d4",
    "Medium":"#f59e0b",
    "Low":"#6b7280"
    }

    for item in results:

        st.markdown(
        f"""
        <div class="card">

        <h3>{item["title"]}</h3>

        <p>{item["summary"]}</p>

        <span class="badge" style="background-color:{sentiment_color[item["sentiment"]]}">
        Sentiment: {item["sentiment"]}
        </span>

        <span class="badge" style="background-color:{impact_color[item["impact"]]}">
        Impact: {item["impact"]}
        </span>

        <br><br>

        <b>Source:</b> {item["source"]}<br>

        <a href="{item["url"]}" target="_blank">Read Full Article</a>

        </div>
        """,
        unsafe_allow_html=True
        )

    # ----------------------------
    # Download Report
    # ----------------------------

    report=""

    for item in results:

        report+=f"{item['title']}\n"
        report+=f"{item['summary']}\n"
        report+=f"Sentiment: {item['sentiment']} | Impact: {item['impact']}\n"
        report+=f"Source: {item['source']}\n"
        report+=f"{item['url']}\n\n"

    st.download_button(
    "📥 Download AI Report",
    report,
    file_name="AI_News_Report.txt"
    )

# ----------------------------
# Footer
# ----------------------------

st.markdown("""
<div class="footer">
Built with ❤️ using Python • Streamlit • FLAN-T5 • NewsAPI • Generative AI
</div>
""", unsafe_allow_html=True)
