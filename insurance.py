import streamlit as st
import pandas as pd
import numpy as np
import plotly_express as px

'''
# An Insurance Statistics WebApp
'''
# Read data from csv file
df = st.cache(pd.read_csv)('Auto_Insurance_Claims_Sample.csv')

# Setting up the sidebar menu
educationLvl = st.sidebar.multiselect(
    'Show clients with education level of:', df['Education'].unique())
states = st.sidebar.multiselect(
    'Show clients living in state:', df['State'].unique())
coverageLvl = st.sidebar.multiselect(
    'Show clients with coverage level:', df['Coverage'].unique())
employeed = st.sidebar.multiselect(
    'Employment status?', df['EmploymentStatus'].unique())
st.sidebar.markdown('Do you want to look up Male or Female clients?')
if st.sidebar.checkbox('Male'):
    df['Gender'].isin(gendMaleChkBx)
if st.sidebar.checkbox('Female'):
    df['Gender'].isin(gendFemChkBx)

# Filter data_frame
if len(educationLvl) == 0:
    educationLvl = df['Education'].unique()
if len(states) == 0:
    states = df['State'].unique()
if len(coverageLvl) == 0:
    coverageLvl = df['Coverage'].unique()
if len(employeed) == 0:
    employeed = df['EmploymentStatus'].unique()

filteredDf = df[(df['Education'].isin(educationLvl)) &
                (df['State'].isin(states)) &
                (df['Coverage'].isin(coverageLvl)) &
                (df['EmploymentStatus'].isin(employeed))]

if st.checkbox('Do you want to see the data?'):
    st.write(df)

if st.checkbox('Do you want to see the filtered data?'):
    st.write(filteredDf)
