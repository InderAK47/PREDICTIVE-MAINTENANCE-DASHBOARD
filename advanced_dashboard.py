
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title='Smart Predictive Maintenance Dashboard',
    layout='wide'
)

st.title('🏭 Smart Predictive Maintenance Dashboard')
st.subheader('AI-Based Bearing Health Monitoring System')

# Read Excel file
df = pd.read_excel(
    "WTP_Predictive_Maintenance_Dummy_Data.xlsx"
)

limits = pd.read_excel(
    "equipments_limits.xlsx"
)

# Clean equipment names
df["Equipment"] = df["Equipment"].astype(str).str.strip()
limits["Equipment"] = limits["Equipment"].astype(str).str.strip()

df = df.dropna()

df["Date"] = pd.to_datetime(df["Date"])

healthy = len(df[df['Health (%)'] >= 70])

warning = len(
    df[
        (df['Health (%)'] >= 50) &
        (df['Health (%)'] < 70)
    ]
)

critical = len(
    df[df['Health (%)'] < 50]
)

a,b,c,d = st.columns(4)

with a:
    st.metric('Total Records',len(df))

with b:
    st.metric('Healthy',healthy)

with c:
    st.metric('Warning',warning)

with d:
    st.metric('Critical',critical)

st.divider()

equipment = st.selectbox(
    "Select Equipment",
    sorted(df["Equipment"].unique())
)

selected = df[
    df["Equipment"] == equipment
]

selected = selected.sort_values(
    "Date"
)

latest = selected.iloc[-1]

# Get limits

limit = limits[
    limits["Equipment"] == equipment
]

if len(limit) > 0:

    max_temp = float(
        limit["MaxTemp"].values[0]
    )

    max_vibration = float(
        limit["MaxVibration"].values[0]
    )

else:

    max_temp = 80
    max_vibration = 5


# Current values

temp = float(
    latest["Temperature"]
)

vib = float(
    latest["Vibration"]
)


# Health calculation

temp_score = 100 - (
    (temp/max_temp)*50
)

vib_score = 100 - (
    (vib/max_vibration)*50
)

health = round(
    (temp_score+vib_score)/2
)

health=max(
    0,
    min(100,health)
)

c1,c2,c3=st.columns(3)

with c1:
    st.metric(
        'Temperature',
        str(latest['Temperature '])
    )

with c2:
    st.metric(
        'Vibration',
        str(latest['Vibration (mm/s)'])+' mm/s'
    )

with c3:
    st.metric(
        'Health',
        str(latest['Health (%)'])+' %'
    )

st.subheader('Temperature Trend')

fig1=px.line(
    selected,
    x='Date',
    y='Temperature '
)

st.plotly_chart(
    fig1,
    use_container_width=True
)

st.subheader('Vibration Trend')

fig2=px.line(
    selected,
    x='Date',
    y='Vibration (mm/s)'
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

st.subheader('Health Trend')

fig3=px.line(
    selected,
    x='Date',
    y='Health (%)'
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

health=latest['Health (%)']

st.subheader('AI Recommendation')

if health<50:
    st.error(
    'High failure probability. Immediate maintenance required.'
    )

elif health<70:
    st.warning(
    'Lubrication and inspection recommended.'
    )

else:
    st.success(
    'Equipment operating normally.'
    )
st.divider()

st.subheader(
"Add New Maintenance Data"
)

with st.form("entry_form"):

    date = st.date_input(
        "Select Date"
    )

    equipment = st.selectbox(
        "Select Equipment",
        sorted(
            df["Equipment"].unique()
        )
    )

    temp = st.number_input(
        "Temperature (°C)",
        min_value=0.0,
        step=0.1
    )

    vibration = st.number_input(
        "Vibration (mm/s)",
        min_value=0.0,
        step=0.1
    )

    health = st.slider(
        "Health (%)",
        0,
        100,
        80
    )

    submit = st.form_submit_button(
        "Submit Data"
    )


if submit:

    new_row = pd.DataFrame({

        "Date":[date],

        "Equipment":[equipment],

        "Temperature(°C)":[temp],

        "Vibration (mm/s)":[vibration],

        "Health (%)":[health]

    })

    df = pd.concat(
        [df,new_row],
        ignore_index=True
    )

    df.to_excel(
        "WTP_Predictive_Maintenance_Dummy_Data.xlsx",
        index=False
    )

    st.success(
    "New data added successfully"
    )
