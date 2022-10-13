import time
from datetime import datetime
from binance.spot import Spot as client
import pandas as pd 
import numpy as np
import plotly.graph_objects as go
import streamlit as st
import tickers as t
from functions import functions as f


allticker = t.tickers

st.set_page_config(
                   page_title = 'pumb_volume.io',
                   page_icon = 'chart_with_upwards_trend',
                   layout = 'wide'
                   
                   )

col2, col3, col4 = st.columns(3)

with col2:
    limit  = st.text_input("Data input :" , "500")
    limit  = int(limit)
with col3:
    value  = st.text_input("Period min :" , "1")
    value  = int(value)
with col4:
    lenght = st.text_input("Data chart :" , "100")
    lenght = int(lenght)


for coin in allticker:
    
    try:
        T , m = f.time_orders_acceleration(coin,limit)
    except:
        T , m = None , None
    
    if (m != None) and (T != None):
        if (T <= value):
            if m <= 0:
                statu = 'BUY'
            else:
                statu = 'SELL'
            
            col2, col3, col4 = st.columns([1,1,3])
            col2.metric("Coin :", coin)
            col3.metric("Statu :", statu)
            
            with col4:
                df  = f.get_data(coin,'1m',lenght)
                fig = f.price_plot(df)
                st.plotly_chart(fig, use_container_width=True)

