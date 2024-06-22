# Import necessary libraries
import streamlit as st
import yfinance as yf
import pandas as pd
import datetime
import numpy as np
from   functions import main_plot, z_score

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
                       start=start, 
                       end=end,
                       interval=interval)
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
st.subheader("**About**")
st.markdown("""
    Stock Volatility Web Application is not a financial advisor

    Copyright 2023 Snowflake Inc. All rights reserved.
    
    \nAuthor @VanHe1sing\n X: https://x.com/sxJEoRg7wwLR6ug\n TradingView: https://www.tradingview.com/u/VanHe1sing/\n Telegram: https://t.me/IvanKocherzhat
    """)

# Render bottom navigation bar content
st.markdown(navbar_bottom, unsafe_allow_html=True)
