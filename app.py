import streamlit as st
import yfinance as yf
import pandas as pd
import pandas_ta as ta

st.set_page_config(page_title="Ultra-Safe Scanner", layout="wide")
st.title("🛡️ High Confirmation Trading Dashboard")
st.write("RSI, EMA 200 සහ MACD දර්ශක මගින් තහවුරු කරන ලද අවස්ථා පමණක් මෙහි පෙන්වයි.")

# කාසි 20 ලැයිස්තුව
coins = [
    'BTC-USD', 'ETH-USD', 'SOL-USD', 'BNB-USD', 'XRP-USD', 
    'ADA-USD', 'AVAX-USD', 'DOGE-USD', 'DOT-USD', 'TRX-USD',
    'LINK-USD', 'MATIC-USD', 'LTC-USD', 'NEAR-USD', 'UNI-USD',
    'APT-USD', 'ARB-USD', 'OP-USD', 'INJ-USD', 'STX-USD'
]

if st.button('සජීවීව Scan කරන්න (Safe Mode)'):
    st.info("ගැඹුරු විශ්ලේෂණයක් සිදු කරමින් පවතී... කරුණාකර තත්පර 30-40ක් රැඳී සිටින්න.")
    
    for symbol in coins:
        try:
            # EMA 200 සඳහා වැඩි දත්ත ප්‍රමාණයක් (period='100d') අවශ්‍ය වේ
            df = yf.download(symbol, period='100d', interval='1h', progress=False)
            
            if not df.empty and len(df) > 200:
                # දර්ශක ගණනය කිරීම
                df['RSI'] = ta.rsi(df['Close'], length=14)
                df['EMA_200'] = ta.ema(df['Close'], length=200)
                
                # MACD ගණනය කිරීම
                macd = ta.macd(df['Close'])
                df = pd.concat([df, macd], axis=1)

                last_row = df.iloc[-1]
                price = float(last_row['Close'])
                rsi = float(last_row['RSI'])
                ema_200 = float(last_row['EMA_200'])
                macd_val = float(last_row['MACD_12_26_9'])
                macd_sig = float(last_row['MACDs_12_26_9'])

                # 🛡️ Ultra-Safe Logic
                plan = "NONE"
                
                # BUY: RSI < 40 + මිල EMA 200 ට ඉහළින් + MACD Bullish (Value > Signal)
                if rsi < 40 and price > ema_200 and macd_val > macd_sig:
                    plan = "BUY"
                
                # SELL: RSI > 60 + මිල EMA 200 ට පහළින් + MACD Bearish (Value < Signal)
                elif rsi > 60 and price < ema_200 and macd_val < macd_sig:
                    plan = "SELL"

                if plan != "NONE":
                    st.markdown(f"### 🎯 {symbol.replace('-USD', '/USDT')}")
                    col1, col2, col3 = st.columns([1, 1, 2])
                    
                    with col1:
                        st.metric("Price", f"${price:,.2f}")
                        st.caption(f"EMA 200: ${ema_200:,.2f}")
                    
                    with col2:
                        if plan == "BUY":
                            st.success(f"🔥 STRONG BUY (RSI: {rsi:.2f})")
                        else:
                            st.error(f"⚠️ STRONG SELL (RSI: {rsi:.2f})")
                    
                    with col3:
                        target = price * 1.05 if plan == "BUY" else price * 0.95
                        sl = price * 0.98 if plan == "BUY" else price * 1.02
                        st.write(f"📍 Entry: **${price:,.2f}**")
                        st.write(f"🎯 Target: **${target:,.2f}**")
                        st.write(f"🛑 SL: **${sl:,.2f}**")
                    st.markdown("---")
            
        except:
            continue
            
    st.success("Scanning අවසන්!")
