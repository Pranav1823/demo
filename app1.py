import streamlit as st
import pandas as pd
import json
import plotly.express as px
import os
from collections import Counter

# --- New Data Loading Functions (Reading Processed and Raw JSON) ---
def load_fund_data(fund_name):
    try:
        with open(r"C:\Users\Pranav\Desktop\HACKATHON\frontend_ui\data\news_VTI_cleaned.json") as f:
            data = json.load(f)
            # Assuming your raw JSON can be directly converted to a DataFrame
            # You might need to adjust this based on the actual structure
            return pd.DataFrame(data)
    except FileNotFoundError:
        st.error(f"Fund data not found for: {fund_name}")
        return None

def load_news_data(fund_name):
    try:
        with open(r"C:\Users\Pranav\Desktop\HACKATHON\frontend_ui\newsensse_output.json") as f:
            return json.load(f)
    except FileNotFoundError:
        st.error(f"News data not found for: {fund_name}")
        return []

# --- Get List of Available Funds ---
def get_available_funds():
    funds = set()
    if os.path.exists("test_data"):
        for filename in os.listdir("test_data"):
            if filename.endswith("_raw.json"):
                fund_name = filename.replace("_raw.json", "")
                funds.add(fund_name)
            elif filename.endswith("_processed.json"):
                fund_name = filename.replace("_processed.json", "")
                funds.add(fund_name)
    return sorted(list(funds))

available_funds = get_available_funds()

# Sidebar
st.sidebar.title("📊 News & Fund Insights")
selected_fund = st.sidebar.selectbox("Select Fund", available_funds)

# Load data for the selected fund
fund_df = load_fund_data(selected_fund)
news_data = load_news_data(selected_fund)

# Main area
st.title(f"Fund Analysis: {selected_fund}")

if fund_df is not None:
    # Fund Performance Chart
    st.subheader("📈 Fund Performance Over Time")
    # Assuming your fund_df has 'date' and 'close' columns. Adjust if needed.
    if 'date' in fund_df.columns and 'close' in fund_df.columns:
        fig_price = px.line(fund_df, x="date", y="close", title=f"{selected_fund} Closing Price Trend")
        fig_price.update_layout(xaxis_title="Date", yaxis_title="Close Price")
        st.plotly_chart(fig_price)
    else:
        st.error("Fund data is missing 'date' or 'close' columns for the chart.")

if news_data:
    # Related News
    st.subheader("📰 Related News")
    for article in news_data:
        # Assuming your news articles have 'title', 'date', 'summary', and 'sentiment' keys. Adjust if needed.
        if 'title' in article and 'date' in article and 'summary' in article and 'sentiment' in article:
            st.markdown(f"**{article['title']}** ({article['date']})")
            st.markdown(f"Sentiment: <span style='color: {'red' if article['sentiment'] == 'negative' else 'green' if article['sentiment'] == 'positive' else 'orange'};'>{article['sentiment'].capitalize()}</span>", unsafe_allow_html=True)
            st.write(article['summary'])
            st.markdown("---")
        else:
            st.warning("A news article is missing required keys.")
else:
    st.info(f"No news found for {selected_fund}")

# User Query Input
st.subheader("🤔 Ask a Question")
user_query = st.text_input("Enter your question about the fund (e.g., 'Why did it drop?')")
if user_query:
    st.info(f"Your query: '{user_query}'. This will be connected to the QA module in the next step.")

if news_data:
    # Sentiment Over Time Chart
    st.subheader("📉 Negative Sentiment Over Time")
    # Assuming your news articles have 'date' and 'sentiment' keys. Adjust if needed.
    negative_news_dates = [article['date'] for article in news_data if 'sentiment' in article and article['sentiment'] == 'negative']
    sentiment_counts = Counter(negative_news_dates)
    sentiment_df = pd.DataFrame(sentiment_counts.items(), columns=['date', 'negative_news_count']).sort_values(by='date')

    if not sentiment_df.empty:
        fig_sentiment = px.line(sentiment_df, x="date", y="negative_news_count",
                                title=f"Negative News Volume for {selected_fund}")
        fig_sentiment.update_layout(xaxis_title="Date", yaxis_title="Number of Negative News")
        st.plotly_chart(fig_sentiment)
    else:
        st.info(f"No negative news found for {selected_fund} to display sentiment over time.")