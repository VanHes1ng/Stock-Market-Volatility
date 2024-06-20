
import plotly.graph_objects as go
import streamlit as st
import numpy as np
import pandas as pd


@st.cache_resource
def get_shades(fig, data):
    below_threshold = data["Z"] < -0.5
    start_indices = data.index[below_threshold]

    for start in start_indices:
        fig.add_shape(
            type="rect",
            x0=start,
            y0=4,
            x1= start - pd.Timedelta(days=1),
            y1=-4,
            line_width=10,
            fillcolor="green",
            opacity=0.05,
            line=dict(
            color="green",
            width=2)

        )

    above_threshold = data["Z"] > 0.5
    start_indices1 = data.index[above_threshold]

    for start in start_indices1:
        fig.add_shape(
            type="rect",
            x0=start,
            y0=4,
            x1= start - pd.Timedelta(days=1),
            y1=-4,
            line_width=10,
            fillcolor="red",
            opacity=0.05,
            line=dict(
            color="red",
            width=2)

        )

def main_plot(data):
        # Create the plot
    fig = go.Figure()

    # Add the first line for Z
    fig.add_trace(go.Scatter(
        x=data.index, 
        y=data["Z"], 
        mode='lines', 
        name='Z',
        line=dict(color='green'),
        yaxis='y1'
    ))

    # Add the second line for SPY with a secondary y-axis
    fig.add_trace(go.Scatter(
        x=data.index, 
        y=data["SPY"], 
        mode='lines', 
        name='SPY',
        line=dict(color='black'),
        yaxis='y2'
    ))
    

    # Add background fill for Z score below -1 using vectorized operations
   
    get_shades(fig, data)

    # Update layout with two y-axes
    fig.update_layout(
        xaxis=dict(title='Index'),

        yaxis=dict(title='Z-Score VIX'),

        yaxis2=dict(title='SPY',overlaying='y',side='right'),

        legend=dict(x=0.1,y=1.1)
    )

    fig.update_layout(
        autosize = False,
        height   = 600
    )
    
    st.plotly_chart(fig, use_container_width=True)


def z_score(src, length):
    #The standard deviation is the square root of the average of the squared deviations from the mean, i.e., std = sqrt(mean(x)), where x = abs(a - a.mean())**2.
    basis = src.rolling(length).mean()
    x = np.abs(src - basis)**2
    stdv = np.sqrt(x.rolling(length).mean())
    z = (src-basis)/ stdv
    return z