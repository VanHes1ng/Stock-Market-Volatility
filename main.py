# Import necessary libraries
import streamlit as st
import yfinance as yf
import pandas as pd
import datetime
import numpy as np
import plotly.graph_objects as go
from functions import main_plot, z_score
import time

# Set up the Streamlit app configuration

st.set_page_config(
    page_title="Stock Market Volatility",
    page_icon="🔃",
    layout="wide",
    initial_sidebar_state="collapsed"
)

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# Hide side bar and collapse control button
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

navbar        = open('components/navbar.txt').read()
vix_          = open('components/vix.txt').read()
desc          = open('components/description.txt').read() 
navbar_bottom = open('components/navbar_bottom.txt').read()



st.markdown(navbar, unsafe_allow_html=True)


# Define a function to download S&P 500 data
@st.cache_data
def download_data(ticker, start, end, interval):
    data = yf.download(ticker, 
                       start    = start, 
                       end      = end,
                       interval = interval)
    return data

col1,  col2,  col3, _  = st.columns([1, 10, 3, 0.5])
col11, col22, col33, _ = st.columns([1, 10, 3, 0.5])


# Inputs
with col3:
    st.write("#")
    st.subheader("Settings")
    
    interval = st.selectbox("TimeFrame", ('1d','5d','1wk','1mo','3mo'))
    year = st.slider("  **Select Start Year:**", 2000, 2023, 2022)
    end_year = st.slider("  **Select End Year:**", 2000, 2030, 2025)

    start_year = datetime.datetime(year, 1, 1)
    end_year = datetime.datetime(end_year, 1, 1)

    set_button = col3.button("Set")
    if set_button:
        # Get data
        spy = download_data("^GSPC", start_year, end=end_year, interval=interval)
        vix = download_data("^VIX", start_year, end=end_year, interval=interval)

        data = pd.DataFrame()
        data["SPY"] = spy["Adj Close"]
        data["VIX"] = vix["Close"]

        data["Z"] = z_score(data["VIX"], 20)



if not set_button:
    st.write("#")
    col2.info('''Set Settings \n
              Selecting big range of data on 1d timeframe can take few minutes to load''', icon="🚨")

if set_button:

    with col2:
        st.subheader("Z-score of VIX and SPY")


        with st.status("Downloading data...", state="running", expanded = False) as status:
  
            main_plot(data)
            status.update(label="Download complete!", state="complete", expanded=True)


        st.write(desc)

    with col22:
        st.markdown("***")
        st.line_chart(data, y = "VIX", color= "#d1a626", height = 300, use_container_width=True)
        

        st.markdown("***")
        with col3:
            z_sc = np.round(data["Z"].iloc[-1], 2)
            delta = np.round(data["Z"].iloc[-1] - data["Z"].iloc[-2], 2)
            st.metric(label="Z-Score", value=z_sc, delta=delta,
            delta_color="normal")


    with col33:
        st.subheader("CBOE Volatility Index")
        st.markdown(vix_)

        st.markdown("***")


st.write("---")
st.subheader("**About**")
st.markdown("""
    Stock Volatility Web Application is not a financial advisor

    Copyright 2023 Snowflake Inc. All rights reserved.
    
    \nAuthor @VanHe1sing\n X: https://x.com/sxJEoRg7wwLR6ug\n TradingView: https://www.tradingview.com/u/VanHe1sing/\n Telegram: https://t.me/IvanKocherzhat
    """)



st.markdown(navbar_bottom, unsafe_allow_html=True)

