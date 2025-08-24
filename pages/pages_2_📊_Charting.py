import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(layout="wide")

if 'data' not in st.session_state:
    st.error("Data not loaded. Please go back to the main app page.")
    st.stop()

data = st.session_state.data.copy() # Use a copy to add indicators

# --- PAGE TITLE & HEADER ---
st.title("Advanced Charting")
st.markdown("Analyze SIMULATED_STOCK with technical indicators.")

# --- SIDEBAR FOR INDICATOR CONTROLS ---
st.sidebar.header("Indicator Settings")
show_sma = st.sidebar.checkbox("Show Simple Moving Average (SMA)", True)
if show_sma:
    sma_short_window = st.sidebar.slider("SMA Short Window", 5, 50, 10)
    sma_long_window = st.sidebar.slider("SMA Long Window", 10, 100, 30)

show_ema = st.sidebar.checkbox("Show Exponential Moving Average (EMA)")
if show_ema:
    ema_window = st.sidebar.slider("EMA Window", 5, 50, 12)

# --- CALCULATE INDICATORS ---
if show_sma:
    data[f'SMA_{sma_short_window}'] = data['Close'].rolling(window=sma_short_window).mean()
    data[f'SMA_{sma_long_window}'] = data['Close'].rolling(window=sma_long_window).mean()

if show_ema:
    data[f'EMA_{ema_window}'] = data['Close'].ewm(span=ema_window, adjust=False).mean()


# --- PLOT THE CHART ---
fig = go.Figure()

# Add Candlestick trace
fig.add_trace(go.Candlestick(x=data.index,
                             open=data['Open'],
                             high=data['High'],
                             low=data['Low'],
                             close=data['Close'],
                             name="Price"))

# Add SMA traces if selected
if show_sma:
    fig.add_trace(go.Scatter(x=data.index, y=data[f'SMA_{sma_short_window}'],
                             line=dict(color='orange', width=1), name=f'SMA {sma_short_window}'))
    fig.add_trace(go.Scatter(x=data.index, y=data[f'SMA_{sma_long_window}'],
                             line=dict(color='cyan', width=1), name=f'SMA {sma_long_window}'))

# Add EMA trace if selected
if show_ema:
    fig.add_trace(go.Scatter(x=data.index, y=data[f'EMA_{ema_window}'],
                             line=dict(color='yellow', width=1), name=f'EMA {ema_window}'))

# Update layout
fig.update_layout(
    title='Interactive Price Chart with Technical Indicators',
    yaxis_title='Price ($)',
    xaxis_title='Date',
    template='plotly_dark',
    height=700,
    xaxis_rangeslider_visible=True
)

st.plotly_chart(fig, use_container_width=True)
