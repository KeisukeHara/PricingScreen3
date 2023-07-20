import streamlit as st
import requests
import json
import matplotlib.pyplot as plt
import numpy as np

# リクエストURL
URL = "https://intfutoppricing.onrender.com/calc/calc_pv/"

# Streamlitアプリの設定
st.title("金利先物オプション時価シミュレーション画面")

# 取引データの入力フォーム
st.header("取引データ入力")
strike_price = st.number_input("ストライク価格(80～120)", value=100.0, step=0.1, format="%f")
expiration_date = st.text_input("オプションの満期日", value="20230914")

# マーケットデータの入力フォーム
st.sidebar.header("マーケットデータ入力")
evaluation_date = st.sidebar.text_input("評価日", value="20230712")
spot_date = st.sidebar.text_input("スポット日", value="20230714")
interest_rate = st.sidebar.number_input("金利", value=0.01, step=0.001, format="%f")
volatility = st.sidebar.number_input("ボラティリティ", value=0.2, step=0.001, format="%f")

# 計算リクエストの準備
body = {
  "trade_data": {
    "trade_id": "string",
    "ccy": "string",
    "strike": strike_price,
    "expiration_date": expiration_date,
    "call_put": "C",
    "buy_sell": "B",
    "amount": 1
  },
  "market_data": {
    "evaluation_date": evaluation_date,
    "spot_date": spot_date,
    "interest_rate": interest_rate,
    "volatility": volatility,
    "underlying_price": 100.0
  }
}

if st.button("計算実行(原資産が80～120で変動する場合のシミュレーション)"):
  x = np.arange(80, 120.1, 0.5) # 原資産価格のリスト
  y = [] #計算結果のリスト(Call)
  z = [] #計算結果のリスト(Put)

  # 計算リクエスト
  for i in x:
    body["market_data"]["underlying_price"] = i
    body["trade_data"]["call_put"] = "C"
    res = requests.post(URL, json.dumps(body))
    y.append(res.json()["premium"])
    body["trade_data"]["call_put"] = "P"
    res = requests.post(URL, json.dumps(body))
    z.append(res.json()["premium"])

  # 計算結果の表示
  st.header("計算結果")
  plt.style.use('ggplot')
  fig, ax = plt.subplots()
  ax.plot(x, y, label="Call")
  ax.plot(x, z, label="Put")
  ax.set_xlabel("underlying")
  ax.set_ylabel("premium")
  ax.legend()
  st.pyplot(fig)