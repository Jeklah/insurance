import streamlit as st
import pandas as pd
import numpy as np
import plotly_express as px

df = pd.read_csv('football_data.csv', encoding='ISO-8859-1')

clubs = st.multiselect('Show Player for Clubs?', df['Club'].unique())
nationalities = st.multiselect(
    'Show Player from Nationalities?', df['Nationality'].unique())

# Filter dataframe
new_df = df[(df['Club'].isin(clubs)) & (df['Nationality'].isin(nationalities))]

# Write dataframe to screen
st.write(new_df)

# Create figure using plotly express
fig = px.scatter(new_df, x='Overall', y='Age', color='Name')

# Plot
st.plotly_chart(fig)
