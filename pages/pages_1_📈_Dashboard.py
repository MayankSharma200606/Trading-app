import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(layout="wide")

# Check if data is loaded in session state
if 'data' not in st.session_state:
    st.error("Data not loaded. Please go back to the main app page.")
    st.stop()

data = st.session_state.data

# --- HELPER FUNCTIONS ---
def get_performance_metrics(df):
    """Calculates key performance metrics for the stock."""
    start_price = df['Close'].iloc[0]
    end_price = df['Close'].iloc[-1]
    total_return = ((end_price - start_price) / start_price) * 100
    annualized_return = total_return * (252 / len(df))
    daily_returns = df['Close'].pct_change()
    volatility = daily_returns.std() * (252 ** 0.5) * 100
    return total_return, annualized_return, volatility

# --- PAGE TITLE & HEADER ---
st.title("Market Dashboard")
st.markdown("An overview of the market and key metrics for SIMULATED_STOCK (AAPL).")

# --- METRICS CARDS ---
total_return, annualized_return, volatility = get_performance_metrics(data)
col1, col2, col3, col4 = st.columns(4)
col1.metric("Current Price", f"${data['Close'].iloc[-1]:.2f}", f"{data['Close'].iloc[-1] - data['Close'].iloc[-2]:.2f}")
col2.metric("Total Return", f"{total_return:.2f}%")
col3.metric("Annualized Return", f"{annualized_return:.2f}%")
col4.metric("Annualized Volatility", f"{volatility:.2f}%")

# --- MAIN CHART ---
st.subheader("Price Chart")

# Create a candlestick chart with volume
fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                    vertical_spacing=0.03, subplot_titles=('Price', 'Volume'),
                    row_width=[0.2, 0.7])

# Candlestick chart
fig.add_trace(go.Candlestick(x=data.index,
                             open=data['Open'],
                             high=data['High'],
                             low=data['Low'],
                             close=data['Close'],
                             name="Price"),
              row=1, col=1)

# Volume bar chart
fig.add_trace(go.Bar(x=data.index, y=data['Volume'], name="Volume", marker_color='rgba(0, 102, 204, 0.6)'),
              row=2, col=1)

# Update layout for a professional look
fig.update_layout(
    title='SIMULATED_STOCK Price and Volume',
    yaxis_title='Price ($)',
    xaxis_rangeslider_visible=False,
    template='plotly_dark',
    height=600,
    showlegend=False
)
fig.update_yaxes(title_text="Volume", row=2, col=1)

st.plotly_chart(fig, use_container_width=True)

# --- ADDITIONAL INFO ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("Recent Data")
    st.dataframe(data.tail(10).sort_index(ascending=False))

with col2:
    st.subheader("Data Summary")
    st.write(data.describe())
