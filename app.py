import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_csv('vehicles_us.csv')
df['manufacturer'] = df['model'].apply(lambda x: x.split()[0])
 
# create a text header above the dataframe
st.header('Data viewer') 
# Streamlit display code
st.title('Vehicle Data Analysis')
# display the dataframe with streamlit
st.dataframe(df)