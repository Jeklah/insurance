import streamlit as st
import pandas as pd
import numpy as np
import plotly_express as px

'''
# Club and Nationality App

This very simple webapp allows you to select and visualize players from certain clubs and certain nationalities.
'''

# works without encoding? maybe a windows thing?
df = st.cache(pd.read_csv)('football_data.csv')
## df = pd.read_csv('football_data.csv', encoding='ISO-8859-1')

clubs = st.sidebar.multiselect('Show Player for Clubs?', df['Club'].unique())
nationalities = st.sidebar.multiselect(
    'Show Player from Nationalities?', df['Nationality'].unique())

# Filter dataframe
new_df = df[(df['Club'].isin(clubs)) & (df['Nationality'].isin(nationalities))]

# Write dataframe to screen
st.write(new_df)

# Create distplot with custom bin_size
fig = px.scatter(new_df, x='Overall', y='Age', color='Name')

'''
### Here is a simple chart between player age and overall.
'''

# Plot
st.plotly_chart(fig)
x
