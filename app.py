import streamlit as st
import yfinance as yf
import pandas as pd
import pandas_ta as ta
import time

st.set_page_config(page_title="Ultimate Crypto Scanner", layout="wide")
st.title("🚀 Smart Trading Signal Dashboard")
st.subheader("Buy & Sell Signals with Entry, SL, TP (RSI Based)")

# කාසි 20 ලැයිස්තුව (ඔයාට අවශ්‍ය නම් තව එකතු කරන්න පුළුවන්)
coins = [
    'BTC-USD', 'ETH-USD', 'SOL-USD', 'BNB-USD', 'XRP-USD', 
    'ADA-USD', 'AVAX-USD', 'DOGE-USD', 'DOT-USD', 'TRX-USD',
    'LINK-USD', 'MATIC-USD', 'LTC-USD', 'NEAR-USD', 'UNI-USD',
    'APT-USD', 'ARB-USD', 'OP-USD', 'INJ-USD', 'STX-USD'
]

if st.button('සජීවීව Scan කරන්න'):
    st.info("වෙළඳපොළ දත්ත පරීක්ෂා කරමින් පවතී...")

    for symbol in coins:
        try:
            # දත්ත ලබාගැනීම
            df = yf.download(symbol, period='5d', interval='1h', progress=False, timeout=10)

            if df.empty:
                ticker = yf.Ticker(symbol)
                df = ticker.history(period='5d', interval='1h')

            if not df.empty and len(df) > 14:
                # Column නම් පිරිසිදු කිරීම
                if isinstance(df.columns, pd.MultiIndex):
                    df.columns = df.columns.get_level_values(0)

                # RSI ගණනය කිරීම
                df['RSI'] = ta.rsi(df['Close'], length=14)

                last_row = df.iloc[-1]
                price = float(last_row['Close'])
                rsi = float(last_row['RSI'])

                st.markdown(f"### {symbol.replace('-USD', '/USDT')}")
                col1, col2, col3 = st.columns([1, 1, 2])

                with col1:
                    st.metric("Price", f"${price:,.2f}")

                with col2:
                    if rsi < 35:
                        st.success(f"🔥 BUY SIGNAL (RSI: {rsi:.2f})")
                        plan = "BUY"
                    elif rsi > 65:
                        st.error(f"⚠️ SELL SIGNAL (RSI: {rsi:.2f})")
                        plan = "SELL"
                    else:
                        st.info(f"Neutral ({rsi:.2f})")
                        plan = "NONE"

                with col3:
                    if plan == "BUY":
                        st.write("**✅ Long (Buy) Plan:**")
                        st.write(f"- 📍 Entry: ${price:,.2f}")
                        st.write(f"- 🎯 Target (TP): ${price * 1.05:,.2f}")
                        st.write(f"- 🛑 Stop Loss (SL): ${price * 0.98:,.2f}")
                    elif plan == "SELL":
                        st.write("**⚠️ Short (Sell) Plan:**")
                        st.write(f"- 📍 Entry: ${price:,.2f}")
                        st.write(f"- 🎯 Target (TP): ${price * 0.95:,.2f}")
                        st.write(f"- 🛑 Stop Loss (SL): ${price * 1.02:,.2f}")
                    else:
                        st.write("පැහැදිලි සිග්නල් එකක් නැත. රැඳී සිටින්න.")
                st.markdown("---")
            
            # Rate limit නොවී සිටීමට තත්පරයක විවේකයක්
            time.sleep(0.5)

        except Exception as e:
            continue
