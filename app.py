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

    # Moving Averages (used in model)
    df['MA_10'] = df['Close'].rolling(10).mean()
    df['MA_50'] = df['Close'].rolling(50).mean()

    # ✅ RSI (NEW FEATURE)
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))

    # Create target
    df['Target'] = df['Close'].shift(-1)
    df = df.dropna()

    from sklearn.ensemble import RandomForestRegressor

    features = ['Close', 'MA_10', 'MA_50', 'RSI']
    X = df[features]
    y = df['Target']

    model = RandomForestRegressor()
    model.fit(X, y)

    # Prediction
    latest = X.iloc[-1].values.reshape(1, -1)
    prediction = model.predict(latest)

    st.subheader("📈 Next Day Prediction")
    st.write(f"Predicted Price: {prediction[0]:.2f}")

    last_price = df['Close'].iloc[-1]

    if prediction[0] > last_price:
        st.success("📈 BUY Signal")
    else:
        st.error("📉 SELL Signal")

    # ✅ RSI DISPLAY (ALWAYS SHOW)
    st.subheader("📉 RSI Indicator")
    st.line_chart(df['RSI'])

    st.write("RSI > 70 = Overbought 🔴")
    st.write("RSI < 30 = Oversold 🟢")

    # Data Preview
    st.subheader("Data Preview")
    st.write(df.head())

    # Closing Price Chart
    if 'Close' in df.columns:
        st.subheader("Stock Closing Price")
        st.line_chart(df['Close'])
    else:
        st.warning("No 'Close' column found in dataset")
