# -*- coding: utf-8 -*-
"""
Created on Wed Aug 26 18:33:24 2020

@author: esteb
"""


import pyodbc

def read_test(conn):
    print("reading connection")
    cursor = conn.cursor()
    cursor.execute("select * from tUserCompetence")
    for row in cursor:
        print(f'row = {row}')
    print()
    

connection = pyodbc.connect(
    "Driver={SQL Server Native Client 11.0};"
    "Server=LAPTOP-MBMTL92H;"
    "Database=SchedulingToolDev;"
    "Trusted_Connection=yes;"
)

read_test(connection)
connection.close()