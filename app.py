import sys
sys.path.append("src")

import streamlit as st
import pandas as pd
import plotly.express as px
from database import DatabaseManager

st.set_page_config(layout="wide")

# ---------------- TITLE ----------------

st.title("NIFTY 50 Stocks Sentiment Analyzer")

st.markdown(
    """
    This dashboard gives users an almost real-time comprehensive visual overview
    on the sentiments of various NIFTY indices.
    """
)

# ---------------- DATABASE ----------------

db_manager = DatabaseManager()

article_data = db_manager.get_articles()
ticker_metadata = db_manager.get_ticker_metadata()

# ---------------- SIDEBAR ----------------

st.sidebar.header("Filters")

date_range = st.sidebar.selectbox(
    "Pick the Date Range",
    ["Past 24 Hours", "Past 7 Days", "Past 1 Month"]
)

# ---------------- DATE FILTER ----------------

article_data["date_posted"] = pd.to_datetime(
    article_data["date_posted"]
)

now = pd.Timestamp.now()

if date_range == "Past 24 Hours":
    filtered_articles = article_data[
        article_data["date_posted"] >= now - pd.Timedelta(hours=24)
    ]

elif date_range == "Past 7 Days":
    filtered_articles = article_data[
        article_data["date_posted"] >= now - pd.Timedelta(days=7)
    ]

else:
    filtered_articles = article_data[
        article_data["date_posted"] >= now - pd.Timedelta(days=30)
    ]

# ---------------- AGGREGATION ----------------

ticker_scores = (
    filtered_articles[
        [
            "ticker",
            "neutral_sentiment",
            "positive_sentiment",
            "negative_sentiment",
            "compound_sentiment",
        ]
    ]
    .groupby("ticker")
    .mean()
    .reset_index()
)

# ---------------- MERGE ----------------

final_df = pd.merge(
    ticker_metadata,
    ticker_scores,
    on="ticker",
    how="inner"
)

# ---------------- RENAME ----------------

final_df.rename(
    columns={
        "mCap": "Market Cap (Billion Rs)",
        "compound_sentiment": "Sentiment Score",
        "neutral_sentiment": "Neutral",
        "positive_sentiment": "Positive",
        "negative_sentiment": "Negative",
    },
    inplace=True,
)

# ---------------- TREEMAP ----------------

fig = px.treemap(
    final_df,
    path=[px.Constant("NIFTY 50"), "sector", "industry", "ticker"],
    values="Market Cap (Billion Rs)",
    color="Sentiment Score",
    hover_data=[
        "companyName",
        "Negative",
        "Neutral",
        "Positive",
        "Sentiment Score",
    ],
    color_continuous_scale=["#FF0000", "#000000", "#00FF00"],
    color_continuous_midpoint=0,
)

fig.data[0].customdata = final_df[
    [
        "companyName",
        "Negative",
        "Neutral",
        "Positive",
        "Sentiment Score",
    ]
]

fig.data[0].texttemplate = "%{label}<br>%{customdata[4]}"

fig.update_traces(textposition="middle center")

fig.update_layout(
    margin=dict(t=30, l=10, r=10, b=10),
    font_size=20,
    paper_bgcolor="#0E1117",
    plot_bgcolor="#0E1117",
    font_color="white",
)

# ---------------- SHOW TREEMAP ----------------

st.plotly_chart(fig, use_container_width=True)

# ---------------- STOCK NEWS ----------------

st.subheader("Stock Specific News")

selected_stock = st.selectbox(
    "Select Stock",
    final_df["ticker"].unique()
)

stock_news = filtered_articles[
    filtered_articles["ticker"] == selected_stock
]

st.dataframe(
    stock_news[
        [
            "headline",
            "source",
            "date_posted",
            "compound_sentiment",
        ]
    ]
)

# ---------------- LAST UPDATE ----------------

st.info(
    f"Last Refreshed: {pd.Timestamp.now().strftime('%d/%m/%Y %H:%M:%S')}"
)
