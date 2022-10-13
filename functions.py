# import Libraries
from binance.spot import Spot as Client
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time
from datetime import date


class functions:
    ###################################################################################################################

    def spot_client_():
        # url to access binance api
        base_url = "https://api.binance.com"

        # use for testing
        base_url_test = "https://testnet.binance.vision"

        # create Client to access API
        spot_client = Client(base_url=base_url)
        return spot_client

    ###################################################################################################################

    def get_data(coin,frame,limit):
      # Access historical prices
      data = functions.spot_client_().klines(coin, frame, limit=limit)
      #display(btcusd_history[:2])

      # show as DataFrame
      columns=['time', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'number_of_trades', 
              'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore']

      dff = pd.DataFrame(data, columns=columns)
      dff['time_ms'] = dff['time']
      dff['time'] = pd.to_datetime(dff['time'], unit='ms')
      df = dff.loc[:, ['time_ms','open','high','low','close','number_of_trades']].copy()
      df = df.set_index(dff['time'])

      df["open"] = pd.to_numeric(df["open"])
      df['close'] = pd.to_numeric(df["close"])
      df ["high"] = pd.to_numeric(df["high"])
      df["low"] = pd.to_numeric(df["low"])
      df["number_of_trades"] = pd.to_numeric(df["number_of_trades"])

      #df = volatility(df)
      df = functions.color(df)
      return df
 


    ###################################################################################################################

    #color
    def color(dff):
      dff['color'] = 0
      dff.loc[(dff['close'] - dff['open'] >= 0), 'color'] = 1
      return dff

    ############################################################################################################ volatility
    def volatility(df):
      #df['volatility'] = ((df['High']-df['Low'])/df['Open'])*100
      df['volatility'] = abs(((100/df['open'])*df['close'])-100)
      df['volatility2'] = ((100/df['open'])*df['close'])-100
      return df

      ############################################################################################################ plot price
    def price_plot(Df):
      candlesticks = go.Candlestick(x=Df.index,open=Df['open'], high=Df['high'], low=Df['low'], close=Df['close'])
      fig = go.Figure(candlesticks)
      #fig.update_layout(paper_bgcolor='black', plot_bgcolor='black',
      #                  margin_l =0, margin_b =0, margin_r =0, margin_t =0)
      fig.update_layout(xaxis_rangeslider_visible=False)
      fig.update_layout(width=150 , height=150, margin_l =0, margin_b =0, margin_r =0, margin_t =0)
      #fig0 = go.Figure(data=[go.Candlestick(x=Df.index, open=Df['open'], high=Df['high'], low=Df['low'], close=Df['close'])])

      return fig
     

        ################################################################################################################### mich

    def mich(df,m):
      #mich up
      c1 = (df['color'] == 0) & ((df['Close'] - df['Low']) > m*(df['Open'] - df['Close'])) & ((df['Close'] - df['Low']) > m*(df['High'] - df['Open']))
      c2 = (df['color'] == 1) & ((df['Open'] - df['Low']) > m*(df['Close'] - df['Open'])) & ((df['Open'] - df['Low']) > m*(df['High'] - df['Close']))
      #c3  = (df['color'] == 1)
      df.loc[c1 | c2, 'vp'] = df['Quote_V']

      #mich down
      c4 = (df['color'] == 0) & ((df['High'] - df['Open']) > m*(df['Open'] - df['Close'])) & ((df['High'] - df['Open']) > m*(df['Close'] - df['Low']))
      c5 = (df['color'] == 1) & ((df['High'] - df['Close']) > m*(df['Close'] - df['Open'])) & ((df['High'] - df['Close']) > m*(df['Open'] - df['Low']))
      #c6  = (df['color'] == 0)
      df.loc[c4 | c5 , 'vn'] = -df['Quote_V']

      return df

        ################################################################################################################### trades

    def time_orders_acceleration(coin,limit):
      dataa = functions.spot_client_().trades(coin,limit=limit)

      L0 = [] 
      L1 = [] 
      L2 = [] 
      D = {} 
      for i in dataa: 
        L0.append(i['time']) 
        L1.append(i['quoteQty'])
        L2.append(i['isBuyerMaker'])
        #print(i)

      D['time'] = L0 
      D['quoteQty'] = L1 
      D['isBuyerMaker'] = L2 
      df_trades = pd.DataFrame(D)
      df_trades['time'] = pd.to_datetime(df_trades['time'],unit='ms')

      df_trades['quoteQty'] = pd.to_numeric(df_trades['quoteQty']) #
      df_trades.loc[(df_trades['isBuyerMaker'] == True) , 'quoteQty'] = -df_trades['quoteQty'] #
      m = df_trades['quoteQty'][-limit:].mean()

      H1 = df_trades['time'][0].hour 
      H2 = df_trades['time'][len(df_trades)-1].hour

      if H2-H1 == 1:
        T1 = 60 - df_trades['time'][0].minute 
        T2 = df_trades['time'][len(df_trades)-1].minute 
        T = T2 + T1
      if H2-H1 == 0:
        T1 = df_trades['time'][0].minute 
        T2 = df_trades['time'][len(df_trades)-1].minute  
        T = T2 - T1

      return T , m #L0  ,df_trades['quoteQty'].to_list()

        ################################################################################################################### mich





