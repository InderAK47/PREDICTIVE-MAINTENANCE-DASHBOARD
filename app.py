
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
page_title="Smart Predictive Maintenance",
layout="wide"
)

st.title("Inderpreet Dashboard")

df=pd.read_csv("machine_data.csv")


# TOP SUMMARY

healthy=len(df[df["Health"]>=70])

warning=len(
df[(df["Health"]>=50) &
(df["Health"]<70)]
)

critical=len(
df[df["Health"]<50]
)

a,b,c=st.columns(3)

with a:
    st.metric(
    "Healthy Machines",
    healthy
    )

with b:
    st.metric(
    "Warning",
    warning
    )

with c:
    st.metric(
    "Critical",
    critical
    )


st.subheader("Machine Status Table")

st.dataframe(df)


machine=st.selectbox(
"Select Machine",
df["Machine"]
)

selected=df[
df["Machine"]==machine
]

st.subheader(
"Machine Details"
)

c1,c2,c3,c4=st.columns(4)

with c1:
    st.metric(
    "Temperature",
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
y=[
"Temperature",
"Vibration",
"Health"
]
)

st.plotly_chart(
fig,
use_container_width=True
)


health=selected["Health"].values[0]


st.subheader(
"AI Recommendation"
)

if health<50:

    st.error(
    "Predicted bearing failure risk high. Schedule shutdown immediately."
    )

elif health<70:

    st.warning(
    "Lubrication and inspection recommended within 5 days."
    )

else:

    st.success(
    "Machine operating normally."
    )

