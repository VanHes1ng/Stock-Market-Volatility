# Import necessary libraries
import streamlit as st
import yfinance as yf
import pandas as pd
import datetime
import numpy as np
from   functions import main_plot, z_score
import matplotlib.pyplot as plt

# Set up the Streamlit app configuration
st.set_page_config(
    page_title              = "Stock Market Volatility",
    page_icon               = "🔃",
    layout                  = "wide",
    initial_sidebar_state   = "collapsed"
)

# CSS to hide Streamlit menu, footer, and header for cleaner UI
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# CSS to hide Streamlit sidebar and collapse control button
st.markdown("""
            <style>
            [data-testid="stSidebar"] {
                visibility: hidden
            }

            [data-testid="collapsedControl"] {
                visibility: hidden
            }
            </style>
            """, unsafe_allow_html=True)

# Load HTML components for navigation and description
navbar         = open('components/navbar.txt').read()
vix_           = open('components/vix.txt').read()
desc           = open('components/description.txt').read()
navbar_bottom  = open('components/navbar_bottom.txt').read()

# Render top navigation bar
st.markdown(navbar, unsafe_allow_html=True)

# Define a function to download S&P 500 data and cache it for optimized performance
@st.cache_data
def download_data(ticker, start, end, interval):
    data = yf.download(ticker, 
                       start    = start, 
                       end      = end,
                       interval = interval)
    return data

# Layout setup using Streamlit columns
col1, col2, col3, _ = st.columns([0.8, 10, 3, 0.4])

# Settings section for user inputs
with col3:
    st.write("#")
    st.subheader("Settings")
    
    # Selectbox for timeframe interval
    interval = st.selectbox("TimeFrame", ('1d', '5d', '1wk', '1mo', '3mo'))
    
    # Slider to select start and end years
    year = st.slider("**Select Start & End Years:**", 2000, 2040, (2022, 2025))
    
    # Divider line
    st.write("---")
    
    # Number input for Z Score Length
    z_len = st.number_input("Z Score Length", 0, 100, 40, step=1)
    
    # Convert selected years to datetime format for data fetching
    start_year = datetime.datetime(year[0], 1, 1)
    end_year   = datetime.datetime(year[1], 1, 1)

    # Fetch data for S&P 500 (^GSPC) and VIX (^VIX)
    spy = download_data("^GSPC", start_year, end=end_year, interval=interval)
    vix = download_data("^VIX", start_year, end=end_year, interval=interval)

    # Prepare DataFrame for data processing
    data = pd.DataFrame()
    data["SPY"] = spy["Adj Close"]
    data["VIX"] = vix["Close"]

    # Calculate Z-score based on VIX data and user-defined length
    data["Z"] = z_score(data["VIX"], z_len)

    # Calculate latest Z-score and delta from previous value
    z_sc  = np.round(data["Z"].iloc[-1], 2)
    delta = np.round(data["Z"].iloc[-1] - data["Z"].iloc[-2], 2)

    # Display Z-score metrics
    st.write("#")
    st.write("#")
    c1, c2, c3 = st.columns([1.5, 1, 1])
    c2.metric(label="Z-Score VIX", value=z_sc, delta=delta, delta_color="normal")

    # Display main content in col2
    with col2:
        # Subheader for Z-score of VIX and SPY
        st.subheader("Z-score of VIX and SPY")

        # Display main plot with data
        main_plot(data)
        
        # Display description text below main plot
        st.write(desc)

        # Divider and additional content
        st.markdown("***")
        st.subheader("CBOE Volatility Index")
        
        # Display line chart for VIX
        st.line_chart(data, y="VIX", color="#d1a626", height=300, use_container_width=True)
        
        # Additional text content
        st.markdown(vix_)

# Render bottom navigation bar
st.write("---")

with st.expander("**About**"):
    st.write('''
        ### Stock Market Volatility Prediction System Overview

        **Purpose:**
        The Stock Market Volatility Prediction System provides valuable insights into future market movements, 
        empowering users to make informed investment decisions without executing trades directly. 
        It utilizes the VIX (CBOE Volatility Index) as a crucial indicator for forecasting trends within the SPY (S&P 500 ETF) market.


        **Key Concepts:**

        1. **Z-Score Definition:**
        - Z-score is a statistical measure that describes a value's relationship to the mean of a group of values. 
            It quantifies how far a particular data point is from the mean in terms of standard deviations.

        2. **Interpreting VIX and Z-Score:**
        - **Decreasing Volatility (Z < 0):** Highlighted on the chart with green shades, indicating a more stable market environment. 
            In this scenario, the system suggests that SPY may potentially experience an upward trend.
        ![plot](components/up_trend.png)
        
        - **Increasing Volatility (Z > 0):** Highlighted on the chart with red shades, signaling potential market turbulence. 
            The system assists users in considering strategies that accommodate potential market downturns.
             
        3. **Investment Strategy Implications:**
        - Users can use this information to explore investment strategies aligned with potential market improvements or downturns, based on the observed trends in VIX and Z-score dynamics.

        **How It Works:**
        - **VIX as a Leading Indicator:** The system leverages the VIX to predict trends in the SPY market. 
            Changes in the VIX provide insights into market sentiment and volatility levels.
        
        - **Real-Time Analysis:** By monitoring the Z-score, users can assess the current volatility status relative to historical norms, facilitating proactive decision-making.

        **Target Audience:**
        - **Investors:** Individuals seeking insights into market volatility trends to inform their investment strategies.
        
        - **Financial Analysts:** Professionals analyzing market data to forecast potential market movements and adjust their recommendations accordingly.

        **Conclusion:**
        The Stock Market Volatility Prediction System enhances decision-making capabilities by offering predictive insights derived from the VIX and Z-score analysis. 
        It equips users with valuable information to navigate market conditions effectively, aligning their investment strategies with anticipated market improvements or downturns.
            ''')

st.markdown("""
    Stock Volatility Web Application is not a financial advisor

    Copyright 2023 Snowflake Inc. All rights reserved.
    
    \nAuthor @VanHe1sing\n X: https://x.com/sxJEoRg7wwLR6ug\n TradingView: https://www.tradingview.com/u/VanHe1sing/\n Telegram: https://t.me/IvanKocherzhat
    """)

# Render bottom navigation bar content
st.markdown(navbar_bottom, unsafe_allow_html=True)
