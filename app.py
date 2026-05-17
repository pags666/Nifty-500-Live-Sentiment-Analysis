import streamlit as st
import os

st.set_page_config(layout="wide")

html_file = "NIFTY_500_live_sentiment.html"

if os.path.exists(html_file):
    with open(html_file, "r", encoding="utf-8") as f:
        html_content = f.read()

    st.components.v1.html(html_content, height=3000, scrolling=True)

else:
    st.error("Dashboard HTML not found.")
