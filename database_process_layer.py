# -*- coding: utf-8 -*-
"""
Created on Tue Sep  1 17:33:29 2020

@author: esteb
"""


import datetime
import database_access as dba
import pandas as pd
import sqlalchemy as sa

def get_tests_week(week_n):
    """
    week: week number of the year
    returns a dataframe of tests whose allowed start dates are all in week_n 
    """
    conn = dba.sqlalchemy_connection()
    test_data = dba.get_tests(conn)
    # list of pandas timestamps corrseponding to the allowedStartDates of the tests
    allowed_start_dates = test_data["AllowedStartDate"]
    # new dataframe where we'll insert the right values
    test_data_week_n = pd.DataFrame(columns=test_data.columns)
    
    test_data["week"] = [val.week for val in test_data["AllowedStartDate"]]
    test_data_week_n = test_data[test_data["week"]==week_n]
    test_data = test_data.drop(labels=["week"],axis=1)   
    test_data_week_n = test_data_week_n.drop(labels=["week"],axis=1)
    
    return test_data_week_n




