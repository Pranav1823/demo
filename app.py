import streamlit as st
import pandas as pd
import json
import altair as alt
from collections import Counter

# Load data
@st.cache_data
def load_fund_data():
    with open(r"C:\Users\Pranav\Desktop\HACKATHON\frontend_ui\data\funds_data.json") as f:
        return pd.read_json(f)

@st.cache_data
def load_news():
    with open(r"C:\Users\Pranav\Desktop\HACKATHON\frontend_ui\data\news\news_corpus.json") as f:
        return json.load(f)

fund_df = load_fund_data()
news_data = load_news()

# Sidebar
st.sidebar.title("📊 News & Fund Insights")
selected_fund = st.sidebar.selectbox("Select Fund", fund_df["ticker"].unique())

# Filter data for the selected fund
fund_filtered = fund_df[fund_df["ticker"] == selected_fund].sort_values(by='date')

# Main area
st.title(f"Fund Analysis: {selected_fund}")

# Fund Performance Chart
st.subheader("📈 Fund Performance Over Time")
fig_price, ax_price = plt.subplots()
ax_price.plot(fund_filtered["date"], fund_filtered["close"], marker='o')
ax_price.set_xlabel("Date")
ax_price.set_ylabel("Close Price")
ax_price.set_title(f"{selected_fund} Closing Price Trend")
plt.xticks(rotation=45)
st.pyplot(fig_price)

# Related News
st.subheader("📰 Related News")
related_news = [article for article in news_data if selected_fund in article.get("tickers", [])]
for article in related_news:
    st.markdown(f"**{article['title']}** ({article['date']})")
    st.markdown(f"Sentiment: <span style='color: {'red' if article['sentiment'] == 'negative' else 'green' if article['sentiment'] == 'positive' else 'orange'};'>{article['sentiment'].capitalize()}</span>", unsafe_allow_html=True)
    st.write(article['summary'])
    st.markdown("---")

if not related_news:
    st.info(f"No news found for {selected_fund}")

# User Query Input
st.subheader("🤔 Ask a Question")
user_query = st.text_input("Enter your question about the fund (e.g., 'Why did it drop?')")
if user_query:
    st.info(f"Your query: '{user_query}'. This will be connected to the QA module in the next step.")

# Sentiment Over Time Chart
st.subheader("📉 Negative Sentiment Over Time")
negative_news_dates = [article['date'] for article in related_news if article['sentiment'] == 'negative']
sentiment_counts = Counter(negative_news_dates)
sentiment_df = pd.DataFrame(sentiment_counts.items(), columns=['date', 'negative_news_count']).sort_values(by='date')

if not sentiment_df.empty:
    fig_sentiment, ax_sentiment = plt.subplots()
    ax_sentiment.plot(sentiment_df["date"], sentiment_df["negative_news_count"], marker='o', color='red')
    ax_sentiment.set_xlabel("Date")
    ax_sentiment.set_ylabel("Number of Negative News")
    ax_sentiment.set_title(f"Negative News Volume for {selected_fund}")
    plt.xticks(rotation=45)
    st.pyplot(fig_sentiment)
else:
    st.info(f"No negative news found for {selected_fund} to display sentiment over time.")
