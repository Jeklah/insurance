import time
import math
import array
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
educationLvl = st.sidebar.multiselect('Show clients with education level of:', df['Education'].unique())
states = st.sidebar.multiselect('Show clients living in state:', df['State'].unique())
coverageLvl = st.sidebar.multiselect('Show clients with coverage level:', df['Coverage'].unique())
employed = st.sidebar.multiselect('Employment status?', df['EmploymentStatus'].unique())

st.sidebar.markdown('Do you want to look up Male or Female clients?')
# If policy age is 0 (default value), no records show up in filtered df, as obv no policies exist with age of 0
policyAgeArrSldVal = st.sidebar.slider('Policy Age in Months:', 0, 120, 0, 1)
policyAgeArr = array.array('i', (range(1, policyAgeArrSldVal+1)))
policyAgeList = policyAgeArr.tolist()
payout = pd.to_numeric(df['Claim Amount'] , downcast='unsigned').tolist()

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
policyInception = df[(df['Months Since Policy Inception'].isin(policyAgeList))]
lastClaim = pd.to_numeric(df['Months Since Last Claim'], downcast='unsigned').tolist()

st.markdown(len(policyInception))
if (len(policyInception) == 0):
    filteredDf = df[(df['Education'].isin(educationLvl)) &
                    (df['State'].isin(states)) &
                    (df['Coverage'].isin(coverageLvl)) &
                    (df['EmploymentStatus'].isin(employed)) &
                    (df['Gender'] == gender)]
else:
    filteredDf = df[(df['Education'].isin(educationLvl)) &
                (df['State'].isin(states)) &
                (df['Coverage'].isin(coverageLvl)) &
                (df['EmploymentStatus'].isin(employed)) &
                (df['Gender'] == gender) &
                (df['Months Since Policy Inception'].isin(policyAgeList))]
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
    # Plotting the graphs
    points & bars

# Graph that took a lot of effort but looks shit with this data/columns.
# Keeping for reference.
if st.checkbox('Would you like to see a histogram for policy age and type against payout?'):
    progressBar = st.progress(0)
    hist_data = [policyAgeList, payout, lastClaim]
    histGrpLabels = ['Policy Age', 'Total Payout', 'Months Since Last Claim']
    fig = ff.create_distplot(hist_data, histGrpLabels, bin_size=[.05, .1, .2])

    st.plotly_chart(fig)

    for percent_complete in range(1, 100):
        time.sleep(0.1)
        progressBar.progress(percent_complete + 1)
