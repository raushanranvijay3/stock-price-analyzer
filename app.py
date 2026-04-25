import streamlit as st
import pandas as pd

st.title("📈 Stock Price Analyzer")

uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.subheader("Data Preview")
    st.write(df.head())

    if 'Close' in df.columns:
        st.subheader("Stock Closing Price")
        st.line_chart(df['Close'])
    else:
        st.warning("No 'Close' column found in dataset")
