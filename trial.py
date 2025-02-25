import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd
import os
from dotenv import load_dotenv

# Load credentials from .env
load_dotenv()
USER_CREDENTIALS = {
    os.getenv("ADMIN_USER"): os.getenv("ADMIN_PASS"),
    os.getenv("USER1"): os.getenv("USER1_PASS"),
}

# Session state for login
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Login form
if not st.session_state.logged_in:
    st.title("🔒 Secure Stock Dashboard")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
            st.session_state.logged_in = True
            st.success("✅ Login successful!")
            st.experimental_rerun()
        else:
            st.error("❌ Invalid username or password")

else:
    # Stock Dashboard
    st.title("📊 Stock Price Dashboard")
    ticker = st.sidebar.text_input("Enter Stock Ticker (e.g., AAPL, TSLA)", "AAPL")
    start_date = st.sidebar.date_input("Start Date", pd.to_datetime("2023-01-01"))
    end_date = st.sidebar.date_input("End Date", pd.to_datetime("today"))

    try:
        stock_data = yf.download(ticker, start=start_date, end=end_date)
        fig = go.Figure(data=[go.Candlestick(
            x=stock_data.index,
            open=stock_data["Open"],
            high=stock_data["High"],
            low=stock_data["Low"],
            close=stock_data["Close"]
        )])
        fig.update_layout(title=f"{ticker} Stock Price", xaxis_title="Date", yaxis_title="Price")
        st.plotly_chart(fig)
    except Exception as e:
        st.error(f"Error fetching data: {e}")

    # Logout button
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.experimental_rerun()
