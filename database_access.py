# -*- coding: utf-8 -*-
"""
Created on Wed Aug 26 18:33:24 2020

@author: Gabriel
"""


import pyodbc
import sqlalchemy as sa
import pandas as pd
import sys

"""
ONLY USABLE FOR A LOCAL SERVER
"""

SERVER = "LAPTOP-MBMTL92H"
DB = "SchedulingToolDev"
DRIVER = "SQL Server Native Client 11.0"
USERNAME = ""
PASSWORD = ""
DB_CONNECTION = f'mssql://{USERNAME}:{PASSWORD}@{SERVER}/{DB}?driver={DRIVER}'

def read_test(conn):
    print("reading connection")
    cursor = conn.cursor()
    cursor.execute("select * from tUserCompetence")
    for row in cursor:
        print(f'row = {row}')
    print()
    
def pyodbc_connect():
    connection = pyodbc.connect(
        "Driver={SQL Server Native Client 11.0};"
        "Server=LAPTOP-MBMTL92H;"
        "Database=SchedulingToolDev;"
        "Trusted_Connection=yes;"
    )
    return connection

def sqlalchemy_connection(server=SERVER,db=DB,driver=DRIVER,username=USERNAME,password=PASSWORD):
    db_connection = f'mssql://{username}:{password}@{server}/{db}?driver={driver}'
    engine = sa.create_engine(db_connection)
    connection = engine.connect()
    return connection


def get_analysts_tests(connection):
    """

    Parameters
    ----------
    connection : sqlalchemy connection
        contains a connection to the database

    Returns a pandas dataframe containing test IDs (of each task) 
    and the list of analysts that can carry it out. 
    This list is only relevant for the first 6 stages of a test, as the last one (review) needs to be 
    carried out by a reviewer (not an analyst).
    In case of exception raised, returns None
    """
    
    query = """
            select 
            tTest.ID,
            tTest.TeamID,
            tUserCompetence.CompetenceID,
            tUserCompetence.UserID
            from tTest
            inner join tProductSpec on tTest.ProductSpecID = tProductSpec.ID
            inner join tUserCompetence on tUserCompetence.CompetenceID = tProductSpec.CompetenceID
            inner join tUser on tUserCompetence.UserID = tUser.ID
            inner join tUserRole on tUser.ID = tUserRole.UserID
            inner join tRole on tRole.ID = tUserRole.RoleID
            where tUser.TeamID = tTest.TeamID and tRole.Name LIKE '%analyst%'
            order by tTest.ID;
            """
    data = None
    try:
        data = pd.read_sql_query(query, connection)  
    except:
        print(sys.exc_info()[0])
    finally:
        return data
    

def get_reviewers(connection):
    """

    Parameters
    ----------
    connection : sqlalchemy connection
        contains a connection to the database

    Returns a pandas dataframe containing test ID (of each task) 
    and the list of reviewers that can carry it out. 
    This list is only relevant for the last of a test, as it needs to be carried out by a reviewer
    (not by an analyst) that is NOT THE SAME PERSON as the analysts who carried out the preceding
    tasks.
    In case of exception raised, returns None
    """

    query = """
            select 
            tTest.ID,
            tTest.TeamID,
            tUserCompetence.CompetenceID,
            tUserCompetence.UserID
            from tTest
            inner join tProductSpec on tTest.ProductSpecID = tProductSpec.ID
            inner join tUserCompetence on tUserCompetence.CompetenceID = tProductSpec.CompetenceID
            inner join tUser on tUserCompetence.UserID = tUser.ID
            inner join tUserRole on tUser.ID = tUserRole.UserID
            inner join tRole on tRole.ID = tUserRole.RoleID
            where tUser.TeamID = tTest.TeamID and tRole.Name LIKE '%reviewer%'
            order by tTest.ID;
            """    
            
    data = None
    try:
        data = pd.read_sql_query(query, connection)  
    except:
        print(sys.exc_info()[0])
    finally:
        return data 
    
    
def get_equipment(connection):
    """
    

    Parameters
    ----------
    connection : sqlalchemy connection
        contains a connection to the database

    Returns a pandas dataframe containing the equipment (machines) able to carry out each task
    (test ID). The SAME MACHINE must be used for every task of each job.
    In case of exception raised, returns None.
    """
    
    query = """
            select 
            tTest.ID as TestID,
            tEquipmentGroup.GroupID, 
            tEquipmentGroup.EquipmentID
            from tTest
            inner join tGroupSpec on tGroupSpec.ProductSpecID = tTest.ProductSpecID
            inner join tEquipmentGroup on tEquipmentGroup.GroupID = tGroupSpec.GroupID
            order by tTest.ID;
            """
    data = None
    try:
        data = pd.read_sql_query(query, connection)  
    except:
        print(sys.exc_info()[0])
    finally:
        return data 

def get_tasks(connection):
    """
    Parameters
    ----------
    connection : sqlalchemy connection
        contains a connection to the database

    Returns a pandas dataframe containing the equipment (machines) able to carry out each task
    (test ID). The SAME MACHINE must be used for every task of each job.
    In case of exception raised, returns None.
    """

    query = """
            select 
            tTest.ID, 
            Phase,
            tProcedureTemplate.Name as PhaseName,
            Time,
            Machine, 
            Persons
            from tTest
            inner join tProcedureTemplate on tProcedureTemplate.ProductSpecID = tTest.ProductSpecID
            order by tTest.ID, Phase;
            """    

    data = None
    try:
        data = pd.read_sql_query(query, connection)  
    except:
        print(sys.exc_info()[0])
    finally:
        return data

def get_tests(connection):
    """
    returns all tests (all jobs) in a dataframe
    """
    
    query = "select * from tTest"
    data = None
    try:
        data = pd.read_sql_query(query, connection)  
    except:
        print(sys.exc_info()[0])
    finally:
        return data 
    
def get_tests_week(week_n):
    """
    week: week number of the year
    returns a dataframe of tests whose allowed start dates are all in week_n 
    """
    conn = sqlalchemy_connection()
    test_data = get_tests(conn)
    # list of pandas timestamps corrseponding to the allowedStartDates of the tests
    allowed_start_dates = test_data["AllowedStartDate"]
    # new dataframe where we'll insert the right values
    test_data_week_n = pd.DataFrame(columns=test_data.columns)
    
    test_data["week"] = [val.week for val in test_data["AllowedStartDate"]]
    test_data_week_n = test_data[test_data["week"]==week_n]
    test_data = test_data.drop(labels=["week"],axis=1)   
    test_data_week_n = test_data_week_n.drop(labels=["week"],axis=1)
    
    return test_data_week_n


def get_shift_users(connection):
    
    """
    Parameters
    ----------
    connection : sql alchemy connection
    returns a pandas dataframe containing the shift hours and the associated 
    analysts and reviewers (users).
    """
    
    query = """
            select * 
            from tShift,tShiftHours
            where tShiftHours.ID = tShift.ShiftHoursID
            """
    
    data = None
    try:
        data = pd.read_sql_query(query, connection)  
    except:
        print(sys.exc_info()[0])
    finally:
        return data





