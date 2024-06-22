# Import necessary libraries
import streamlit as st
import yfinance as yf
import pandas as pd
import datetime
import numpy as np
import plotly.graph_objects as go
from functions import main_plot, z_score


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

# Inputs
with col3:
    st.write("#")
    st.subheader("Settings")
    
    interval = st.selectbox("TimeFrame", ('1d','5d','1wk','1mo','3mo'))
    year  = st.slider("  **Select Start & End Years:**", 2000, 2040, (2022, 2025))
    z_len = st.number_input("Z Score Length", 0, 100, 40, step=1)
    start_year = datetime.datetime(year[0], 1, 1)
    end_year   = datetime.datetime(year[1], 1, 1)

    # Get data
    spy = download_data("^GSPC", start_year, end=end_year, interval=interval)
    vix = download_data("^VIX", start_year, end=end_year, interval=interval)

    data = pd.DataFrame()
    data["SPY"] = spy["Adj Close"]
    data["VIX"] = vix["Close"]

    data["Z"] = z_score(data["VIX"], z_len)

    z_sc = np.round(data["Z"].iloc[-1], 2)
    delta = np.round(data["Z"].iloc[-1] - data["Z"].iloc[-2], 2)

    st.write("#")
    c1, c2, c3 = st.columns([1, 1, 1])

    c2.metric(label="Z-Score", value=z_sc, delta=delta,delta_color="normal")

  

    with col2:
        st.subheader("Z-score of VIX and SPY")

        main_plot(data)
        st.write(desc)

        st.markdown("***")
        st.subheader("CBOE Volatility Index")
        st.line_chart(data, y = "VIX", color= "#d1a626", height = 300, use_container_width=True)
        st.markdown(vix_)





st.write("---")
st.subheader("**About**")
st.markdown("""
    Stock Volatility Web Application is not a financial advisor

    Copyright 2023 Snowflake Inc. All rights reserved.
    
    \nAuthor @VanHe1sing\n X: https://x.com/sxJEoRg7wwLR6ug\n TradingView: https://www.tradingview.com/u/VanHe1sing/\n Telegram: https://t.me/IvanKocherzhat
    """)



st.markdown(navbar_bottom, unsafe_allow_html=True)
