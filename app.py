import streamlit as st
import pandas as pd

st.title("📈 Stock Price Analyzer")

uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # Convert Date
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'])
        df = df.sort_values('Date')

    # Sidebar filter
    st.sidebar.title("Controls")

    if 'Ticker' in df.columns:
        ticker = st.sidebar.selectbox("Select Stock", df['Ticker'].unique())
        df = df[df['Ticker'] == ticker]

    st.subheader("Data Preview")
    st.write(df.head())

    if 'Close' in df.columns:
        st.subheader("Stock Closing Price")
        st.line_chart(df['Close'])
    else:
        st.warning("No 'Close' column found in dataset")
