import streamlit as st
import pandas as pd
import numpy as np

df = pd.read_csv('football_data.csv', encoding='ISO-8859-1')

clubs = st.multiselect('Show Player for Clubs?', df['Club'].unique())
nationalities = st.multiselect('Show Player from Nationalities?', df['Nationality'].unique())

# Filter dataframe
new_df = df[(df['Club'].isin(clubs)) & (df['Nationality'].isin(nationalities))]

# Write dataframe to screen
st.write(new_df)