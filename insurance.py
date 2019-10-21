import streamlit as st
import pandas as pd
import numpy as np
import plotly_express as px
import altair as alt

'''
# An Insurance Statistics WebApp
'''
# Read data from csv file
df = st.cache(pd.read_csv)('Auto_Insurance_Claims_Sample.csv')
gender = df['Gender']

# Setting up the sidebar menu
educationLvl = st.sidebar.multiselect(
    'Show clients with education level of:', df['Education'].unique())
states = st.sidebar.multiselect(
    'Show clients living in state:', df['State'].unique())
coverageLvl = st.sidebar.multiselect(
    'Show clients with coverage level:', df['Coverage'].unique())
employed = st.sidebar.multiselect(
    'Employment status?', df['EmploymentStatus'].unique())
st.sidebar.markdown('Do you want to look up Male or Female clients?')

# Filter data_frame
if len(educationLvl) == 0:
    educationLvl = df['Education'].unique()
if len(states) == 0:
    states = df['State'].unique()
if len(coverageLvl) == 0:
    coverageLvl = df['Coverage'].unique()
if len(employed) == 0:
    employed = df['EmploymentStatus'].unique()
if st.sidebar.checkbox('Male'):
    gender = 'M'
if st.sidebar.checkbox('Female'):
    gender = 'F'

filteredDf = df[(df['Education'].isin(educationLvl)) &
                (df['State'].isin(states)) &
                (df['Coverage'].isin(coverageLvl)) &
                (df['EmploymentStatus'].isin(employed)) &
                (df['Gender'] == gender)]

if st.checkbox('Do you want to see the data?'):
    st.write(df)

if st.checkbox('Do you want to see the filtered data?'):
    st.write(filteredDf)


# scatter graph with histogram depending on whats selected in the scatter graph.
if st.checkbox('Would you like to see a comparison between total claim amount and months since last claim?'):
    brush = alt.selection(type='interval')
    points = alt.Chart(df).mark_point().encode(
        x='Months Since Last Claim',
        y='Total Claim Amount',
        color=alt.condition(brush, 'Total Claim Amount',
                            alt.value('lightgrey'))
    ).add_selection(
        brush
    )
    bars = alt.Chart(df).mark_bar().encode(
        y='Months Since Last Claim:N',
        color='Months Since Last Claim:N',
        x='count(Total Claim Amount):Q'
    ).transform_filter(
        brush
    )
    points & bars
