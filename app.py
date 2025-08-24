import streamlit as st
import pandas as pd
import time

# --- PAGE CONFIGURATION ---
# Set the layout to wide, give it a title and an icon.
st.set_page_config(
    page_title="AlgoTrader Pro",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM STYLING ---
# Inject custom CSS to make the app look more like a professional trading platform.
# This includes a dark theme, specific fonts, and styled widgets.
st.markdown("""
<style>
    /* Main app styling */
    .main {
        background-color: #0E1117;
        color: #FAFAFA;
    }
    /* Sidebar styling */
    .st-emotion-cache-16txtl3 {
        background-color: #161A25;
    }
    /* Metric cards styling */
    .st-emotion-cache-1r6slb0 {
        border: 1px solid #262730;
        border-radius: 0.5rem;
        padding: 1rem;
        background-color: #161A25;
    }
    /* Chart styling */
    .stPlotlyChart {
        border-radius: 0.5rem;
    }
    /* Buttons styling */
    .stButton>button {
        border-radius: 0.5rem;
        background-color: #0066CC;
        color: white;
        border: none;
    }
    .stButton>button:hover {
        background-color: #0052A3;
    }
</style>
""", unsafe_allow_html=True)


# --- DATA LOADING & CACHING ---
# Cache the data loading to improve performance.
# The app will only reload the data if the file changes.
@st.cache_data
def load_data(file_path):
    """
    Loads stock data from a CSV file into a pandas DataFrame.
    Sets the 'Date' column as the index.
    """
    try:
        df = pd.read_csv(file_path)
        df['Date'] = pd.to_datetime(df['Date'])
        df.set_index('Date', inplace=True)
        return df
    except FileNotFoundError:
        st.error(f"Error: The file {file_path} was not found. Please make sure it's in the correct directory.")
        return None

# Load the data into session state to be accessible across pages.
if 'data' not in st.session_state:
    data = load_data('MOCK_DATA.csv')
    if data is not None:
        st.session_state.data = data
    else:
        # Stop the app if data loading fails
        st.stop()

# --- SIDEBAR NAVIGATION & CONTENT ---
st.sidebar.title("AlgoTrader Pro")
st.sidebar.write("Welcome to your personal trading dashboard.")

# --- Live Market Clock ---
st.sidebar.subheader("Market Clock")
clock_placeholder = st.sidebar.empty()

# --- Main Page Content ---
# This is the landing page content before navigating to other pages.
st.title("Welcome to AlgoTrader Pro")
st.write("""
This platform is your all-in-one solution for developing, backtesting, and simulating algorithmic trading strategies.
Navigate through the pages using the sidebar to access different tools.
""")
st.info("Please select a page from the sidebar to get started.", icon="👈")


# --- DYNAMIC ELEMENTS ---
# This loop keeps the clock in the sidebar updated.
while True:
    current_time = time.strftime("%H:%M:%S")
    clock_placeholder.metric("Current Time (UTC)", current_time)
    time.sleep(1)
