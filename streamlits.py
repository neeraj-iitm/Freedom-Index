import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random
import hfi_utils

import pickle 
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go




@st.cache
def load_data(name="HFI_Countries.pickle"):
    df = pickle.load(open(name, "rb"))
    index = list(df['INDIA'].index)
    columns = list(df['INDIA'].columns)
    return df, index, columns

@st.cache
def proc_data(A, B):
    A.columns = columns
    B.columns = columns
    change = A.sub(B, axis='columns')
    pct_change = A.sub(B, axis='columns').div(B)*100
    
    return change,pct_change


df, index, columns = load_data()


st.title("Human Freedom Index Analysis")
st.markdown("This application is a Human Freedom Index Dashboard for Various Countries:")

st.sidebar.title("Select Report Type")
report_type = st.sidebar.selectbox('What do you want to do?', ['Explore Countrywise','Perform Comparision'], key='1')
keys = hfi_utils.get_country_names()

if report_type == 'Explore Countrywise':
    st.sidebar.title("Select Country & Indicator")
    
    select_country = st.sidebar.selectbox('Select Country to View Performance', keys)
    select_parameter = st.sidebar.selectbox('Select Indicator to show', columns)
    
    data=df[select_country]
    
    fig, ax = plt.subplots()
    ax.plot(data.index, data[select_parameter], color ='black', marker='o')
    
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    plt.xlabel("Year")
    plt.ylabel(select_parameter)
    plt.title(f"{select_parameter}  in  {select_country.title()}")
    if select_parameter != 'Ranking':
        plt.ylim((0,10.5))
    st.pyplot(fig)

else:
    st.sidebar.title("Select Countries & Parameter")
    
    select_first_country = st.sidebar.selectbox('Select First Country', keys)
    
    select_second_country = st.sidebar.selectbox('Select Second Country', keys[keys!=select_first_country])
    select_parameter = st.sidebar.selectbox('Select Indicator to Compare', columns)
    select_metric = st.sidebar.selectbox('Select Metric', ['Difference','Percent Difference','Vertical Bars'])
    param = select_parameter
    change,pct_change = proc_data(df[select_first_country], df[select_second_country])
    
    
    if select_metric == 'Difference':
        
        fig, ax = plt.subplots()
        as1 = plt.plot(change[param],color ='orange', marker='o')
        plt.xlabel('Years')
        plt.ylabel(f"Difference in \n'{param}'")
        plt.title('Difference in "' + param + "' of " +select_first_country+ ' as compared to ' + select_second_country)   
        plt.show()
        st.pyplot(fig)

    elif select_metric == 'Percent Difference':
        st.markdown(f"*See bottom")
        fig, ax = plt.subplots()
        as2 = plt.plot(pct_change[param],color ='orange', marker='o')
        plt.xlabel('Years')
        plt.ylabel(f"% Difference in \n'{param}'")
        
        plt.title('Percent Difference in \n"' + param + "' of \n" +select_first_country+ ' as compared to ' + select_second_country)   
        plt.show()
        st.pyplot(fig)
        st.markdown(f"Percent difference is calculated on the basis of scores of SECOND selected country i.e. {select_second_country}. \n In other words {select_first_country.title()} performed {pct_change[param].iloc[0]:.2f} % better (or worse, if negative) than {select_second_country.title()} in 2008.")

    else :

        fig, ax = plt.subplots()
        indexs = np.arange(2008,2019)
        bar_width = 0.35
        opacity = 0.8

        rects1 = plt.bar(indexs, df[select_first_country][param], bar_width, label=select_first_country.title()) 
        rects2 = plt.bar(indexs + bar_width, df[select_second_country][param], bar_width, label=select_second_country.title())

        plt.xlabel('Years')
        plt.ylabel(param)
        plt.title('Comparision of \n' +select_first_country+ ' with ' + select_second_country + '\n on ' + "'"+ param + "'")
        plt.xticks(indexs + bar_width, tuple(index))
        
        # plt.legend(bbox_to_anchor=(1.25, 1))
        ax.legend(loc='upper right', bbox_to_anchor=(1.25, 1))
        if param == 'Ranking':
            maxs =max(df[select_first_country][param].max(),df[select_second_country][param].max())+10
            plt.ylim(0,maxs)
        else:
            plt.ylim(0,10.9)
            plt.yticks(range(0,11))
        plt.show()
        st.pyplot(fig)






        
        
        