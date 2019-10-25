import streamlit as st
import pandas as pd
import numpy as np
import plotly_express as px
import altair as alt
import plotly.figure_factory as ff

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
policyAge = st.sidebar.slider('Policy Age in Months:', 0, 120, 0, 1)

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
                (df['Gender'] == gender) &
                (df['Months Since Policy Inception'] == policyAge)]

if st.checkbox('Do you want to see the data?'):
    st.write(df)

if st.checkbox('Do you want to see the filtered data?'):
    st.write(filteredDf)


# scatter graph with histogram depending on whats selected in the scatter graph.
if st.checkbox('Would you like to see a comparison between total claim amount and months since last claim?'):
    if st.checkbox('Would you like to use the current filter for the chart?'):
        chartDf=filteredDf
    else:
        chartDf=df
    brush = alt.selection(type='interval')
    points = alt.Chart(chartDf).mark_point().encode(
        x='Months Since Last Claim',
        y='Total Claim Amount',
        color=alt.condition(brush, 'Policy Type',
                            alt.ColorValue('grey')),
        tooltip=['Total Claim Amount', 'Months Since Last Claim', 'Policy Type']
    ).add_selection(
        brush
    ).properties(
        width=650,
        height=650
    )

    bars = alt.Chart(chartDf).mark_bar().encode(
        y='Months Since Last Claim:N',
        color='Policy Type',
        x='count(Total Claim Amount):Q',
        tooltip=['Total Claim Amount', 'Months Since Last Claim']
    ).transform_filter(
        brush
    ).properties(
        width=800
    )
    points & bars

# histogram with lines for policy age against payout and policy type
if st.checkbox('Would you like to see a histogram for policy age and type against payout?'):
    policyType = df['Policy Type']
    st.echo policyType
    payout = df['Claim Amount']

    hist_data = [policyAge, policyType, payout]

    histGrpLabels = ['Policy Age', 'Policy Type', 'Total Payout']

    fig = ff.create_distplot(hist_data, histGrpLabels, bin_size=[0, 25, 120])

    st.plotly_chart(fig)
