import os
import requests
from typing import List
from dotenv import load_dotenv
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from textblob import TextBlob

load_dotenv()
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

# ----------------------------
# Load Generative AI Model
# ----------------------------
model_name = "google/flan-t5-small"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)


# ----------------------------
# Fetch News Articles
# ----------------------------
def fetch_news(query: str):

    url = f"https://newsapi.org/v2/everything?q={query}&language=en&pageSize=10&apiKey={NEWS_API_KEY}"

    response = requests.get(url)
    data = response.json()

    articles = []

    for article in data.get("articles", []):

        content = article.get("description") or article.get("title")

        if content and content.strip():
            articles.append({
                "title": article.get("title"),
                "content": content.strip(),
                "source": article["source"]["name"],
                "url": article.get("url")
            })

    # remove duplicates
    unique_articles = []
    seen = set()

    for article in articles:
        if article["content"] not in seen:
            unique_articles.append(article)
            seen.add(article["content"])

    return unique_articles[:5]


# ----------------------------
# LangGraph-style AI Pipeline
# ----------------------------
def analyze_articles(articles: List[dict]):

    results = []

    for article in articles:

        inputs = tokenizer(
            f"Summarize: {article['content']}",
            return_tensors="pt",
            max_length=512,
            truncation=True
        )

        outputs = model.generate(**inputs, max_length=60)
        summary = tokenizer.decode(outputs[0], skip_special_tokens=True)

        polarity = TextBlob(summary).sentiment.polarity

        if polarity > 0.2:
            sentiment = "Positive"
        elif polarity < -0.2:
            sentiment = "Negative"
        else:
            sentiment = "Neutral"

        word_count = len(summary.split())

        if word_count > 20:
            impact = "High"
        elif word_count > 12:
            impact = "Medium"
        else:
            impact = "Low"

        results.append({
            "title": article["title"],
            "summary": summary,
            "sentiment": sentiment,
            "impact": impact,
            "source": article["source"],
            "url": article["url"]
        })

    return results