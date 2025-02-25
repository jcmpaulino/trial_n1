import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd

# Streamlit app title
st.title("Stock Price Dashboard 📈")

# Sidebar for user input
ticker = st.sidebar.text_input("Enter Stock Ticker (e.g., AAPL, TSLA)", "AAPL")
start_date = st.sidebar.date_input("Start Date", value=pd.to_datetime("2023-01-01"))
end_date = st.sidebar.date_input("End Date", value=pd.to_datetime("today"))

# Fetch data from Yahoo Finance
try:
    stock_data = yf.download(ticker, start=start_date, end=end_date)

    # Plot candlestick chart
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
