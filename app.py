
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
page_title="Smart Predictive Maintenance",
layout="wide"
)

st.title("AI Based Bearing Health Dashboard")

df=pd.read_csv("machine_data.csv")

col1,col2,col3=st.columns(3)

with col1:
    st.metric(
    "Machines Monitored",
    len(df)
    )

with col2:
    critical=len(df[df["Health"]<50])

    st.metric(
    "Critical Machines",
    critical
    )

with col3:
    avg=df["Health"].mean()

    st.metric(
    "Avg Health",
    str(round(avg,1))+"%"
    )

st.subheader("Machine Status Table")

st.dataframe(df)

machine=st.selectbox(
"Select Machine",
df["Machine"]
)

selected=df[df["Machine"]==machine]

st.subheader("Machine Details")

c1,c2,c3,c4=st.columns(4)

with c1:
    st.metric(
    "Temp",
    str(selected["Temperature"].values[0])+" °C"
    )

with c2:
    st.metric(
    "Vibration",
    str(selected["Vibration"].values[0])+" mm/s"
    )

with c3:
    st.metric(
    "Health",
    str(selected["Health"].values[0])+"%"
    )

with c4:
    st.metric(
    "Remaining Life",
    str(selected["Remaining_Days"].values[0])+" Days"
    )

fig=px.bar(
selected,
x="Machine",
y=["Temperature","Vibration","Health"]
)

st.plotly_chart(
fig,
use_container_width=True
)

health=selected["Health"].values[0]

if health<50:
    st.error(
    "CRITICAL: Maintenance immediately required"
    )

elif health<70:
    st.warning(
    "Attention Required"
    )

else:
    st.success(
    "Machine Healthy"
    )
