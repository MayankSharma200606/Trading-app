import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(layout="wide")

if 'data' not in st.session_state:
    st.error("Data not loaded. Please go back to the main app page.")
    st.stop()

data = st.session_state.data

# --- BACKTESTING LOGIC ---
def run_sma_crossover_backtest(df, short_window, long_window, initial_capital):
    """
    Runs a simple moving average crossover backtest.
    Returns equity curve, trades, and performance metrics.
    """
    signals = pd.DataFrame(index=df.index)
    signals['signal'] = 0.0

    # Create short and long simple moving averages
    signals['short_mavg'] = df['Close'].rolling(window=short_window, min_periods=1, center=False).mean()
    signals['long_mavg'] = df['Close'].rolling(window=long_window, min_periods=1, center=False).mean()

    # Generate signals
    signals['signal'][short_window:] = \
        (signals['short_mavg'][short_window:] > signals['long_mavg'][short_window:]).astype(float)

    # Generate trading orders
    signals['positions'] = signals['signal'].diff()

    # --- Simulate Portfolio ---
    positions = pd.DataFrame(index=signals.index).fillna(0.0)
    positions['Stock'] = 100 * signals['positions'] # Buy/sell 100 shares
    portfolio = positions.multiply(df['Close'], axis=0)
    pos_diff = positions.diff()

    portfolio['holdings'] = (positions.multiply(df['Close'], axis=0)).sum(axis=1)
    portfolio['cash'] = initial_capital - (pos_diff.multiply(df['Close'], axis=0)).sum(axis=1).cumsum()
    portfolio['total'] = portfolio['cash'] + portfolio['holdings']
    portfolio['returns'] = portfolio['total'].pct_change()

    # --- Extract Trades for Plotting ---
    trades = signals[signals['positions'] != 0]

    return portfolio, trades

# --- PAGE UI ---
st.title("Strategy Backtester")

# --- CONFIGURATION ---
st.header("Configuration")
col1, col2, col3 = st.columns(3)
with col1:
    initial_capital = st.number_input("Initial Capital", min_value=1000, value=100000, step=1000)
with col2:
    short_window = st.slider("Short SMA Window", 5, 50, 10)
with col3:
    long_window = st.slider("Long SMA Window", 20, 100, 40)

# --- RUN BACKTEST ---
if st.button("Run Backtest", use_container_width=True):
    if short_window >= long_window:
        st.error("Short window must be smaller than long window.")
    else:
        with st.spinner("Running backtest..."):
            portfolio, trades = run_sma_crossover_backtest(data, short_window, long_window, initial_capital)

            # --- DISPLAY RESULTS ---
            st.header("Results")

            # Performance Metrics
            final_value = portfolio['total'].iloc[-1]
            total_return = (final_value - initial_capital) / initial_capital * 100
            sharpe_ratio = (portfolio['returns'].mean() / portfolio['returns'].std()) * (252**0.5)

            metric1, metric2, metric3 = st.columns(3)
            metric1.metric("Final Portfolio Value", f"${final_value:,.2f}")
            metric2.metric("Total Return", f"{total_return:.2f}%")
            metric3.metric("Annualized Sharpe Ratio", f"{sharpe_ratio:.2f}")

            # Equity Curve Chart
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=portfolio.index, y=portfolio['total'], name='Equity Curve'))
            fig.update_layout(title="Portfolio Equity Curve", template='plotly_dark', height=500)
            st.plotly_chart(fig, use_container_width=True)

            # Trades Log
            st.subheader("Trades Log")
            st.write(f"Total Trades: {len(trades)}")
            st.dataframe(trades[trades['positions'] != 0])
