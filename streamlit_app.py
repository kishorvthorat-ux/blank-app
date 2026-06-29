import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

st.title("📊 Trading Performance Dashboard")

uploaded_file = st.file_uploader("Upload trading_output.xlsx", type=["xlsx"])

if uploaded_file:
    calc = pd.read_excel(uploaded_file, sheet_name="Calculated")
    stats = pd.read_excel(uploaded_file, sheet_name="Stats")

    # ===============================
    # KPIs
    # ===============================
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Trades", int(stats['Total'][0]))
    col2.metric("Wins", int(stats['Wins'][0]))
    col3.metric("Losses", int(stats['Losses'][0]))
    col4.metric("Net PnL", round(stats['Net PnL'][0], 2))

    # ===============================
    # EQUITY CURVE
    # ===============================
    st.subheader("Equity Curve")

    fig_equity = px.line(calc, y="Equity", title="Equity Growth")
    st.plotly_chart(fig_equity, use_container_width=True)

    # ===============================
    # PNL DISTRIBUTION
    # ===============================
    st.subheader("PnL Distribution")

    fig_hist = px.histogram(calc, x="Net PnL", nbins=30)
    st.plotly_chart(fig_hist, use_container_width=True)

    # ===============================
    # WIN / LOSS
    # ===============================
    st.subheader("Win vs Loss")

    win_loss = calc['Net PnL'].apply(lambda x: "Win" if x > 0 else "Loss")
    fig_pie = px.pie(values=win_loss.value_counts(),
                     names=win_loss.value_counts().index)
    st.plotly_chart(fig_pie)

    # ===============================
    # MONTHLY PNL
    # ===============================
    st.subheader("Monthly Performance")

    calc['Month'] = calc['Entry Date'].dt.to_period('M').astype(str)
    monthly = calc.groupby('Month')['Net PnL'].sum().reset_index()

    fig_month = px.bar(monthly, x='Month', y='Net PnL', title="Monthly PnL")
    st.plotly_chart(fig_month, use_container_width=True)
