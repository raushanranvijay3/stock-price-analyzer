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
        # Moving Averages
    df['MA_10'] = df['Close'].rolling(10).mean()
    df['MA_50'] = df['Close'].rolling(50).mean()

    # RSI
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))

    # MACD
    exp1 = df['Close'].ewm(span=12, adjust=False).mean()
    exp2 = df['Close'].ewm(span=26, adjust=False).mean()
    df['MACD'] = exp1 - exp2
    # Create target
    df['Target'] = df['Close'].shift(-1)
    df = df.dropna()

    from sklearn.ensemble import RandomForestRegressor

    features = ['Close', 'MA_10', 'MA_50', 'RSI', 'MACD']
    X = df[features]
    y = df['Target']

    model = RandomForestRegressor()
    model.fit(X, y)

    # Predict next day
    latest = X.iloc[-1].values.reshape(1, -1)
    prediction = model.predict(latest)
    st.subheader("📈 Next Day Prediction")
    st.write(f"Predicted Price: {prediction[0]:.2f}")

    last_price = df['Close'].iloc[-1]

    if prediction[0] > last_price:
        st.success("📈 BUY Signal")
    else:
        st.error("📉 SELL Signal"

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
