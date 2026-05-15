
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
    'WTP_Predictive_Maintenance_Dummy_Data.xlsx'
)

df = df.dropna()

df['Date'] = pd.to_datetime(df['Date'])

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

equipment=st.selectbox(
    'Select Equipment',
    sorted(df['Equipment'].unique())
)

selected=df[
    df['Equipment']==equipment
]

latest=selected.iloc[-1]

st.subheader('Equipment Details')

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
    y='Temperature'
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
