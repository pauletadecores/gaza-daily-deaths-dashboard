"""
Daily Deaths Monitor — Gaza
Author: Paula Souto

This Streamlit dashboard uses data from the TechForPalestine collective,
via the open-source [Palestine API](https://github.com/ummahrican/palestine-api).

Data sources include the Gaza Ministry of Health, the Gaza Government Media Office, and UN OCHA.
The statistics reflect casualties directly attributable to the genocide in Gaza.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import requests

# -------------------------------
# Configuração da página e tema
# -------------------------------
st.set_page_config(page_title="Daily Deaths Monitor — Gaza", layout="wide")

st.set_page_config(page_title="Daily Death Monitor — Gaza", layout="wide")

st.title("Daily Death Monitor — Gaza")
st.caption("Dashboard data provided by [TechForPalestine](https://techforpalestine.org/) via [Palestine API](https://github.com/ummahrican/palestine-api), including the 'Daily Casualties - Gaza' and 'Killed in Gaza' datasets.")

# -------------------------------
# Sidebar
# -------------------------------
with st.sidebar:
    st.header("Settings")
    window = st.number_input("Moving average (days)", min_value=1, max_value=30, value=7)
    refresh = st.button("🔄 Refresh data")

# -------------------------------
# Load data
# -------------------------------
@st.cache_data
def load_data():
    killed_url = "https://data.techforpalestine.org/api/v2/killed-in-gaza.min.json"
    casualties_url = "https://data.techforpalestine.org/api/v2/casualties_daily.min.json"

    df_killed = pd.DataFrame(requests.get(killed_url).json())
    for col in ['age', 'sex']:
        if col not in df_killed.columns:
            df_killed[col] = None

    df_casualties = pd.DataFrame(requests.get(casualties_url).json())
    df_casualties['report_date'] = pd.to_datetime(df_casualties['report_date'], errors='coerce')

    return df_killed, df_casualties

if refresh:
    load_data.clear()

df_killed, df_casualties = load_data()

# -------------------------------
# Filter by date
# -------------------------------
min_date = df_casualties['report_date'].min().date()
max_date = df_casualties['report_date'].max().date()

start_date, end_date = st.slider(
    "Select date range:",
    min_value=min_date,
    max_value=max_date,
    value=(min_date, max_date)
)

df_casualties_filtered = df_casualties[
    (df_casualties['report_date'].dt.date >= start_date) &
    (df_casualties['report_date'].dt.date <= end_date)
]

# -------------------------------
# Daily deaths series
# -------------------------------
daily = df_casualties_filtered[['report_date', 'killed_cum']].copy()
daily['deaths'] = daily['killed_cum'].diff().fillna(daily['killed_cum'])
daily['ma'] = daily['deaths'].rolling(window=window, min_periods=1).mean()
# -------------------------------
# Casualties by Age (histogram)
# -------------------------------
st.subheader("📊 Casualties by Age")

# Create a series counting deaths per age
age_counts = df_killed['age'].dropna().astype(int)
fig_age = px.histogram(
    age_counts,
    x=age_counts,
    nbins=111,  # ages 0 to 110
    labels={'x': 'Age', 'y': 'Deaths'},
    title="Casualties by Age",
)

# Customize layout
fig_age.update_traces(marker_color='#FF4136')  # same color as cumulative deaths curve
fig_age.update_layout(
    template='plotly_dark',
    xaxis=dict(title='Age', range=[0, 110]),
    yaxis=dict(title='Number of Deaths'),
    bargap=0.1
)

st.plotly_chart(fig_age, config={"responsive": True})

# -------------------------------
# Daily deaths table
# -------------------------------
st.subheader("📅 Daily Deaths Table")
daily_table = daily[['report_date', 'deaths', 'killed_cum']].copy()
daily_table.columns = ['Date', 'Deaths', 'Cumulative Deaths']
st.dataframe(daily_table.sort_values('Date', ascending=False), width='stretch')

# -------------------------------
# Cumulative deaths curve
# -------------------------------
fig_cum = go.Figure()
fig_cum.add_trace(go.Scatter(
    x=df_casualties_filtered['report_date'],
    y=df_casualties_filtered['killed_cum'],
    mode='lines',
    line=dict(color='#FF4136', width=3),
    fill='tozeroy',
    name='Cumulative deaths'
))
fig_cum.update_layout(
    template='plotly_dark',
    title="📈 Cumulative Deaths Curve in Gaza",
    xaxis_title="Date",
    yaxis_title="Total Cumulative Deaths",
    hovermode='x unified'
)
st.plotly_chart(fig_cum, config={"responsive": True})

# -------------------------------
# Metrics cards
# -------------------------------
col1, col2, col3, col4, col5 = st.columns(5)

total_latest = df_casualties['killed_cum'].max()
col1.metric("Total deaths", f"{int(total_latest):,}")

children_count = df_killed[df_killed['age'] < 18].shape[0]
col2.metric("Children", f"{children_count:,}")

men_count = df_killed[df_killed['sex'] == 'm'].shape[0]
col3.metric("Men", f"{men_count:,}")

women_count = df_killed[df_killed['sex'] == 'f'].shape[0]
col4.metric("Women", f"{women_count:,}")

injured_total = df_casualties['injured_cum'].max() if 'injured_cum' in df_casualties.columns else 0
col5.metric("Cumulative Injured", f"{int(injured_total):,}")

# -------------------------------
# Pie chart with Vivid palette
# -------------------------------
def categorize(row):
    if pd.isna(row['age']):
        return 'Others'
    if row['age'] < 18:
        return 'Children'
    elif row['sex'] == 'f':
        return 'Women'
    elif row['age'] >= 60:
        return 'Seniors'
    else:
        return 'Others'

df_killed['category'] = df_killed.apply(categorize, axis=1)
category_counts = df_killed['category'].value_counts().reset_index()
category_counts.columns = ['Category', 'Deaths']

fig_pie = px.pie(
    category_counts,
    names='Category',
    values='Deaths',
    title="Death Distribution by Category",
    hole=0.3,
    color_discrete_sequence=px.colors.qualitative.Vivid
)

fig_pie.update_traces(
    textposition='inside',
    textinfo='percent+label',
    textfont=dict(size=20),
    pull=[0.05]*len(category_counts)
)

fig_pie.update_layout(
    height=700,
    width=800,
    template='plotly_dark',
    title_font=dict(size=22),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.2,
        xanchor="center",
        x=0.5,
        font=dict(size=16)
    )
)

st.plotly_chart(fig_pie, config={"responsive": True})

st.markdown("""
---
This dashboard was created using publicly available data compiled from the **Gaza Ministry of Health**, the **Gaza Government Media Office**, and **UN OCHA**.  
The statistics reflect casualties directly attributable to the ongoing genocide and are updated regularly.  

It was inspired by the [Genocide Monitor](https://genocidemonitor.com/) project.  
For more detailed and continuously updated information, please visit their website.
""")
