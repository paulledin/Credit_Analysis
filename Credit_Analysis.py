# -*- coding: utf-8 -*-
"""
Created on Mon Aug 26 14:34:26 2024

@author: PLedin
"""

import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

#from st_oauth import st_oauth

st.set_page_config(
    page_title="America's Credit Unions",
    layout="wide",
    initial_sidebar_state="expanded")

thePassPhrase = st.secrets["thePassPhrase"]
#dbConn = st.connection("snowflake")

###############################################################################
#Function Definitions
###############################################################################
def convertDateToDisplay(date):
    switcher = {
        "01": "January",
        "02": "February",
        "03": "March",
        "04": "April",
        "05": "May",
        "06": "June",
        "07": "July",
        "08": "August",
        "09": "September",
        "10": "October",
        "11": "November",
        "12": "December",
    }
    
    return switcher.get(date[4:], "**Bad Month**") + "-" + date[:4]

def convertDateToSystem(date):
    switcher = {
        "January":  "01",
        "February": "02",
        "March":    "03",
        "April":    "04",
        "May":      "05",
        "June":     "06",
        "July":     "07",
        "August":   "08",
        "September":"09",
        "October":  "10",
        "November": "11",
        "December": "12",
    }
    
    return date[len(date)-4:len(date)] + switcher.get(date[:len(date)-5], "**Bad Month**")

def get_report_periods():
    periods = pd.read_csv('https://raw.githubusercontent.com/paulledin/data/master/MonthlyReportPeriods.csv')
    
    retVal = list()
    index = 0
    for x in periods:
        retVal.insert(index, periods[x])
        index += 1
    
    return (retVal)

def getMergersTable(month):
    df_mergers_table = pd.DataFrame(pd.read_csv('https://raw.githubusercontent.com/paulledin/data/master/merged_cus_' + convertDateToSystem(month) + '.csv', dtype={
                                                'NIMBLE_CUNA_ID': 'string',
                                                'NAME': 'string',
                                                'State': 'string',
                                                'Assets': 'int64',
                                                'Members': 'int64',
                                                'Employees': 'int64',
                                                'SURVIVOR_ID': 'string',
                                                'STATUS_CHG_DATE': 'string'
                                                }))
    df_mergers_table.rename(columns={'SURVIVOR_ID' : 'Survivor NIMBLE_CUNA_ID', 'STATUS_CHG_DATE' : 'Status Change Date'}, inplace=True)
    
    return (df_mergers_table)

def getPendingTable(month):
    return pd.DataFrame(pd.read_csv('https://raw.githubusercontent.com/paulledin/data/master/pending_cus_' + convertDateToSystem(month) + '.csv', dtype={
                                    'NIMBLE_CUNA_ID': 'string',
                                    'NAME': 'string',
                                    'State': 'string',
                                    'Assets': 'int64',
                                    'Members': 'int64',
                                    'Employees': 'int64'
                                    }))

def getLiquidationsTable(month):
    return pd.DataFrame(pd.read_csv('https://raw.githubusercontent.com/paulledin/data/master/liquidated_cus_' + convertDateToSystem(month) + '.csv', dtype={
                                    'NIMBLE_CUNA_ID': 'string',
                                    'NAME': 'string',
                                    'State': 'string',
                                    'Assets': 'int64',
                                    'Members': 'int64',
                                    'Employees': 'int64'
                                    }))

def getNameChgsTable(month):
    return pd.DataFrame(pd.read_csv('https://raw.githubusercontent.com/paulledin/data/master/name_chgs_' + convertDateToSystem(month) + '.csv', dtype={
                                    'NIMBLE_CUNA_ID': 'string',
                                    'Old Name': 'string',
                                    'State': 'string',
                                    'New Name': 'string'
                                    }))

def getCEOChgsTable(month):
    return pd.DataFrame(pd.read_csv('https://raw.githubusercontent.com/paulledin/data/master/ceo_chgs_' + convertDateToSystem(month) + '.csv', dtype={
                                    'NIMBLE_CUNA_ID': 'string',
                                    'Name': 'string',
                                    'State': 'string',
                                    'Old Manager': 'string',
                                    'New Manager': 'string'
                                    }))

def getAddressChgsTable(month, addressType):
    if (addressType == 'mailing'):
        df_address_chgs = pd.DataFrame(pd.read_csv('https://raw.githubusercontent.com/paulledin/data/master/mailing_address_chgs_' + convertDateToSystem(month) + '.csv', dtype={
                                                   'NIMBLE_CUNA_ID': 'string',
                                                   'Name': 'string',
                                                   'Old Mailing Address': 'string',
                                                   'New Mailing Address': 'string'
                                                   }))
    else:
        df_address_chgs = pd.DataFrame(pd.read_csv('https://raw.githubusercontent.com/paulledin/data/master/street_address_chgs_' + convertDateToSystem(month) + '.csv', dtype={
                                                   'NIMBLE_CUNA_ID': 'string',
                                                   'Name': 'string',
                                                   'Old Street Address': 'string',
                                                   'New Street Address': 'string'
                                                   }))
    return df_address_chgs

def getAFLChgsTables(month, aflChgType, aflType):
    if (aflChgType == 'REAFL'):
        df_afl_chgs = pd.DataFrame(pd.read_csv('https://raw.githubusercontent.com/paulledin/data/master/reafl_chgs_' + aflType + '_' + convertDateToSystem(month) + '.csv', dtype={
                                               'NIMBLE_CUNA_ID': 'string',
                                               'Name': 'string',
                                               'State': 'string',
                                               'Assets': 'int64',
                                               'Members': 'int64',
                                               'Employees': 'int64'
                                               }))
    elif (aflChgType == 'DISAFL'):
        df_afl_chgs = pd.DataFrame(pd.read_csv('https://raw.githubusercontent.com/paulledin/data/master/disafl_chgs_' + aflType + '_' + convertDateToSystem(month) + '.csv', dtype={
                                               'NIMBLE_CUNA_ID': 'string',
                                               'Name': 'string',
                                               'State': 'string',
                                               'Assets': 'int64',
                                               'Members': 'int64',
                                               'Employees': 'int64'
                                               }))
    return df_afl_chgs

def getCharterChgsTable(month):
    return pd.DataFrame(pd.read_csv('https://raw.githubusercontent.com/paulledin/data/master/charter_chgs_' + convertDateToSystem(month) + '.csv', dtype={
                                    'NIMBLE_CUNA_ID': 'string',
                                    'Name': 'string',
                                    'Old Charter': 'string',
                                    'Old Charter Type': 'string',
                                    'New Charter': 'string',
                                    'New Charter Type': 'string',
                                    }))

def getNewCUsTable(month):
    return pd.DataFrame(pd.read_csv('https://raw.githubusercontent.com/paulledin/data/master/new_cus_' + convertDateToSystem(month) + '.csv', dtype={
                                    'NIMBLE_CUNA_ID': 'string',
                                    'Name': 'string',
                                    'Address': 'string',
                                    'City': 'string',
                                    'State': 'string',
                                    'Zip Code': 'string'
                                    }))

def getAFLTable(month, aflType):
    if (aflType == 'cuna'):
        df_afl_table = pd.DataFrame(pd.read_csv('https://raw.githubusercontent.com/paulledin/data/master/afl_table_1_ByState_Legacycuna_' + convertDateToSystem(month) + '.csv'))
    elif (aflType == 'nafcu'):
        df_afl_table = pd.DataFrame(pd.read_csv('https://raw.githubusercontent.com/paulledin/data/master/afl_table_1_ByState_Legacynafcu_' + convertDateToSystem(month) + '.csv'))
    else:
        df_afl_table = pd.DataFrame(pd.read_csv('https://raw.githubusercontent.com/paulledin/data/master/afl_table_1_ByState_Either_' + convertDateToSystem(month) + '.csv'))
        
    return df_afl_table

def getPreviousSystemMonth(month):
    system_month = int(convertDateToSystem(month)[4:])
    prev_system_year = convertDateToSystem(month)[:4]
    
    prev_system_month = system_month - 1
    if(prev_system_month == 0):
        prev_system_month = 12
        prev_system_year = str(int(prev_system_year) - 1)
           
    return (prev_system_year + str(prev_system_month).rjust(2, '0'))

def get_report_periods_for_display():
    periods = pd.read_csv('https://raw.githubusercontent.com/paulledin/data/master/MonthlyReportPeriods.csv')    
    retVal = list()

    index = 0
    for x in periods:
        retVal.insert(index, periods[x])
        index += 1
        
    df_retVal = pd.DataFrame(retVal[0])
        
    for i in range(len(df_retVal)):
        period = df_retVal.loc[i, "period"]
        df_retVal.loc[df_retVal['period'] == period, 'report_periods_formatted'] = convertDateToDisplay(str(period))

    return df_retVal
    
def format_number(amount):
    return '{:,.0f}'.format(amount)

def get_report_periods_for_display_from_db():
    periods = get_report_periods_from_db()
    periods['report_periods_formatted'] = periods.apply(lambda row: convertDateToDisplay(str(row.PERIOD)), axis=1)                                                             
    
    return (periods)

@st.cache_data
def get_report_periods_from_db():
    return (dbConn.session().sql("SELECT DISTINCT(SUBSTR(TABLE_NAME, LENGTH(TABLE_NAME)-5, length(TABLE_NAME))) AS period FROM monthly_report.information_schema.tables WHERE table_schema!='INFORMATION_SCHEMA' ORDER BY SUBSTR(TABLE_NAME, LENGTH(TABLE_NAME)-5, LENGTH(TABLE_NAME)) DESC").to_pandas())

@st.cache_data
def getAFLTable_from_db(month, afl_type):
    sqlStmt = "SELECT * FROM monthly_report."
    
    if(afl_type == 'Legacy CUNA'):
        aflType = 'Legacycuna'
    elif(afl_type == 'Legacy NAFCU'):
        aflType = 'Legacynafcu'
    elif(afl_type == 'Member of Both'):
        aflType = 'Both'
    else:
        aflType = 'Either'
    sqlStmt += aflType + '.afl_table_1_ByState' + '_' + convertDateToSystem(month)
    
    return (dbConn.session().sql(sqlStmt).to_pandas())

@st.cache_data
def getChangeTableFromDB(month, table_name):
    sqlStmt = "SELECT * FROM monthly_report.change_reports."
    
    if(table_name == 'mergers'):
        sqlStmt += 'merged_cus' + '_' + convertDateToSystem(month)
    elif(table_name == 'pending'):
        sqlStmt += 'pending_cus' + '_' + convertDateToSystem(month)
    elif(table_name == 'liquidations'):
        sqlStmt += 'liquidated_cus' + '_' + convertDateToSystem(month)
    elif(table_name == 'name_chgs'):
        sqlStmt += 'name_chgs' + '_' + convertDateToSystem(month)
    elif(table_name == 'mailing_address_chgs'):
        sqlStmt += 'mailing_address_chgs' + '_' + convertDateToSystem(month)
    elif(table_name == 'street_address_chgs'):
        sqlStmt += 'street_address_chgs' + '_' + convertDateToSystem(month)
    elif(table_name == 'ceo_chgs'):
        sqlStmt += 'ceo_chgs' + '_' + convertDateToSystem(month)
    elif(table_name == 'charter_chgs'):
        sqlStmt += 'charter_chgs' + '_' + convertDateToSystem(month)
    elif(table_name == 'new_cus'):
        sqlStmt += 'new_cus' + '_' + convertDateToSystem(month)

    return (dbConn.session().sql(sqlStmt).to_pandas())

@st.cache_data
def getAFLChgsTableFromDB(month, chg_type, afl_type):
    sqlStmt = "SELECT * FROM monthly_report.change_reports."
    
    if(chg_type == 'REAFL'):
        sqlStmt += "reafl_chgs_" + afl_type + "_" + convertDateToSystem(month) 
    elif(chg_type == 'DISAFL'):
        sqlStmt += "disafl_chgs_" + afl_type + "_" + convertDateToSystem(month) 

    return (dbConn.session().sql(sqlStmt).to_pandas())
###############################################################################
#Start building Streamlit App
###############################################################################
#report_periods = get_report_periods_for_display_from_db()
report_periods = get_report_periods_for_display()

with st.sidebar:
    st.markdown('![alt text](https://raw.githubusercontent.com/paulledin/data/master/ACUS.jpg)')
    passphrase = st.text_input("### Please enter the passphrase:")

if (passphrase != thePassPhrase):
    if len(passphrase) > 0:
        st.markdown('# Passphrase not correct....')
        st.markdown('### Please try again or contact: pledin@americascreditunions.org for assistance.')
else:  
    column_configuration = {
        "Assets": st.column_config.NumberColumn(
        "Assets ($)",
        help="Total Assets",
        min_value=0,
        max_value=1000000000000,
        step=1,
        format="localized",),
        "Members": st.column_config.NumberColumn(
        "Members",
        help="Number of Memberships",
        min_value=0,
        max_value=1000000000000,
        step=1,
        format="localized",),
        "Employees": st.column_config.NumberColumn(
        "Employees",
        help="Number of Total Employees",
        min_value=0,
        max_value=1000000000000,
        step=1,
        format="localized",)
        }
     
    with st.sidebar:
        st.title('Credit Analysis Reports')
    
        report_type = ['2 Year Summary','Page 2', 'Page 3&4']
        selected_report_type = st.selectbox('Report Type', report_type)

    st.markdown("""<center>America's Credit Unions - Economics and Statistics</center>""", unsafe_allow_html=True)

    if (selected_report_type == '2 Year Summary'):
        st.markdown("""<center>Two-Year Financial Comparison</center>""", unsafe_allow_html=True)
    elif (selected_report_type == 'Page 2'):
        st.markdown("""<center>Credit Analysis - Page 2</center>""", unsafe_allow_html=True)
    elif (selected_report_type == 'Page 3&4'):
        st.markdown("""<center>Credit Analysis - Page 3&4</center>""", unsafe_allow_html=True)

    st.markdown("""<center>All Data As Of: </center>""", unsafe_allow_html=True)
    st.markdown('---')

    col = st.columns((2, 2, 2, 2), gap='small', vertical_alignment='center')
    with col[0]:
        st.markdown('')

    with col[1]:          
        st.markdown("""<center>XYZ Credit Union</center>""", unsafe_allow_html=True)
        st.markdown("""<center>12345 Credit Union Blvd</center>""", unsafe_allow_html=True)
        st.markdown("""<center>Madison, WI</center>""", unsafe_allow_html=True)

    with col[2]:
        st.markdown("""<center>ACUs ID: 100XXXXXX</center>""", unsafe_allow_html=True)
        st.markdown("""<center>Routing #: XXXXXXXXX</center>""", unsafe_allow_html=True)
        st.markdown("""<center>Charter #: XXXXX</center>""", unsafe_allow_html=True)
    
    with col[3]:
        st.markdown('')

    st.markdown('---')

    if (selected_report_type == '2 Year Summary'):
        col = st.columns((2.25, 2, 2, 1, 0.25, 2.25, 2, 2, 1), gap='small')
        with col[0]:
            st.markdown("""<div style="text-align: left;">Assets</div>""", unsafe_allow_html=True)
            st.markdown('---')
            st.markdown('Cash & Equivalents')
            st.markdown('Government Securities')
            st.markdown('Fed Agency Securities')
            st.markdown('Corporate CUs')
            st.markdown('Bank Deposits')
            st.markdown('Mutual Funds')
            st.markdown('All Other Investments')
            st.markdown('---')
            st.markdown('Total Invs excl Cash&Equivs')
            st.markdown('---')
        
        with col[1]:
            st.markdown("""<div style="text-align: right;">YYYY-1</div>""", unsafe_allow_html=True)
            st.markdown('---')
        
        with col[2]:
            st.markdown("""<div style="text-align: right;">YYYY-2</div>""", unsafe_allow_html=True)
            st.markdown('---')

        with col[3]:
            st.markdown("""<div style="text-align: right;">% Chg</div>""", unsafe_allow_html=True)
            st.markdown('---')
        
        with col[4]:
            st.markdown('')
        
        with col[5]:
            st.markdown("""<div style="text-align: left;">Liabilities & Capital</div>""", unsafe_allow_html=True)
            st.markdown('---')
            st.markdown('Reverse Repos')
            st.markdown('Other Notes Payable')
            st.markdown('All Other Liabilities')
            st.markdown('---')
            st.markdown('Total Liabilities')
            st.markdown('---')

        with col[6]:
            st.markdown("""<div style="text-align: right;">YYYY-1</div>""", unsafe_allow_html=True)
            st.markdown('---')
        
        with col[7]:
            st.markdown("""<div style="text-align: right;">YYYY-2</div>""", unsafe_allow_html=True)
            st.markdown('---')

        with col[8]:
            st.markdown("""<div style="text-align: right;">% Chg</div>""", unsafe_allow_html=True)
            st.markdown('---')







