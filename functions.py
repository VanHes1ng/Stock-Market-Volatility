
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def main_plot(data):
    # Sample data with datetime index
    df = pd.DataFrame(data)

    # Create the plot with two y-axes
    fig, ax1 = plt.subplots(figsize=(10, 4), dpi=100)

    # Plot Z on the first y-axis
    color="green"
    ax1.set_xlabel('Date', fontsize=5)
    ax1.set_ylabel('Z', color=color, fontsize=5)
    ax1.plot(df.index, df["Z"], color=color, linewidth=0.5)
    ax1.tick_params(axis='y', labelcolor=color, labelsize=5)
    ax1.tick_params(axis='x', labelsize=5)  # Adjust x-axis tick label size
    # Add a dashed horizontal line at Z = 0
    ax1.axhline(y=0, color='gray', linestyle='--', linewidth=0.5)

    # Fill background where Z is below -1
    ax1.fill_between(df.index, -4, 4, where=(df["Z"] <= 0), color='green', alpha=0.3, linewidth=0)
    ax1.fill_between(df.index, 4, -4, where=(df["Z"] > 0), color='red', alpha=0.3, linewidth=0)

    # Create a second y-axis
    ax2 = ax1.twinx()
    color = "black"
    ax2.set_ylabel('SPY', color=color, fontsize=5)
    ax2.plot(df.index, df["SPY"], color=color, linewidth=1)
    ax2.tick_params(axis='y', labelcolor=color, labelsize=5)

    st.pyplot(fig, use_container_width=True)


def z_score(src, length):
    #The standard deviation is the square root of the average of the squared deviations from the mean, i.e., std = sqrt(mean(x)), where x = abs(a - a.mean())**2.
    basis = src.rolling(length).mean()
    x = np.abs(src - basis)**2
    stdv = np.sqrt(x.rolling(length).mean())
    z = (src-basis)/ stdv
    return z