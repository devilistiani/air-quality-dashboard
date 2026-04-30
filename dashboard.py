import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

sns.set(style='dark')

def create_monthly_pm25_df(df):
    monthly_pm25_df = df.resample(rule='ME', on='datetime').agg({
        "PM2.5": "mean"
    })
    monthly_pm25_df.index = monthly_pm25_df.index.strftime('%B %Y')
    monthly_pm25_df = monthly_pm25_df.reset_index()
    return monthly_pm25_df

def create_station_pm25_df(df):
    station_pm25_df = df.groupby("station")["PM2.5"].mean().sort_values(ascending=False).reset_index()
    return station_pm25_df

all_df = pd.read_csv("main_data.csv")
all_df["datetime"] = pd.to_datetime(all_df["datetime"])
all_df.sort_values(by="datetime", inplace=True)
all_df.reset_index(inplace=True)

min_date = all_df["datetime"].min()
max_date = all_df["datetime"].max()

with st.sidebar:
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = all_df[(all_df["datetime"] >= str(start_date)) & 
                (all_df["datetime"] <= str(end_date))]

monthly_pm25_df = create_monthly_pm25_df(main_df)
station_pm25_df = create_station_pm25_df(main_df)

st.header('Beijing Air Quality Dashboard :cloud:')

# Tren Polusi PM2.5
st.subheader('Tren Konsentrasi PM2.5 Bulanan')

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    monthly_pm25_df["datetime"],
    monthly_pm25_df["PM2.5"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15, rotation=45)
st.pyplot(fig)

# Perbandingan Polusi antar Stasiun & Korelasi Cuaca
st.subheader('Kualitas Udara antar Stasiun Pengamatan')

col1, col2 = st.columns(2)

with col1:
    avg_pm25 = main_df["PM2.5"].mean()
    st.metric("Rata-rata PM2.5 (μg/m³)", value=round(avg_pm25, 2))

with col2:
    worst_station = station_pm25_df.iloc[0]["station"]
    st.metric("Stasiun Polusi Tertinggi", value=worst_station)

fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(
    y="PM2.5", 
    x="station",
    data=station_pm25_df,
    palette="viridis",
    ax=ax
)
ax.set_title("Rata-rata Konsentrasi PM2.5 Berdasarkan Stasiun", loc="center", fontsize=15)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='x', labelsize=12, rotation=45)
st.pyplot(fig)

st.subheader('Korelasi Cuaca terhadap PM2.5')
fig, ax = plt.subplots(figsize=(10, 6))
corr = main_df[['PM2.5', 'TEMP', 'RAIN', 'WSPM']].corr()
sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f", ax=ax)
st.pyplot(fig)

st.caption('Copyright (c) Devi Listiani Safitri 2026')