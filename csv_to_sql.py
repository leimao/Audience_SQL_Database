# Audience Data Preprocessing and Import
# Author: Lei Mao
# Date: 4/5/2017

# Data source format
'''
Data categories:
customer_ID, name, gender, ID, passport_ID, phone_number, project, expense, spouse_ID, children_ID, relatives_ID, friends_ID, notes

The data were separated by tab.

The encoding of the data needs to be UTF-8.
'''


import sqlite3
import os
import re
import time

customer_data_file = 'customer_data.txt'

project_data_file = 'project_data.txt'

current_year = time.localtime()[0]

conn = sqlite3.connect("dalian_tv_database.sqlite3")
# UTF-8 support
conn.text_factory = str

cur = conn.cursor()

# Create Customer_Data table
cur.execute('DROP TABLE IF EXISTS Customer_Data')
cur.execute('CREATE TABLE Customer_Data (Customer_ID INTEGER, Name TEXT, Gender TEXT, Age TEXT, ID TEXT, Passport_ID TEXT, Phone_Number TEXT, Notes TEXT)')

# Create Spouse_Relation table
cur.execute('DROP TABLE IF EXISTS Spouse_Relation')
cur.execute('CREATE TABLE Spouse_Relation (Customer_ID INTEGER, Spouse_ID INTEGER)')

# Create Children_Relation table
cur.execute('DROP TABLE IF EXISTS Children_Relation')
cur.execute('CREATE TABLE Children_Relation (Customer_ID INTEGER, Children_ID INTEGER)')

# Create Relatives_Relation table
cur.execute('DROP TABLE IF EXISTS Relatives_Relation')
cur.execute('CREATE TABLE Relatives_Relation (Customer_ID INTEGER, Relatives_ID INTEGER)')

# Create Friends_Relation table
cur.execute('DROP TABLE IF EXISTS Friends_Relation')
cur.execute('CREATE TABLE Friends_Relation (Customer_ID INTEGER, Friends_ID INTEGER)')

# Create Project_Participants table
cur.execute('DROP TABLE IF EXISTS Project_Participants')
cur.execute('CREATE TABLE Project_Participants (Customer_ID INTEGER, Project_ID INTEGER, Expense INTEGER)')

# Create Project_Data table
cur.execute('DROP TABLE IF EXISTS Project_Data')
cur.execute('CREATE TABLE Project_Data (Project_ID INTEGER, Project_Name TEXT, Price INTEGER, Size INTEGER, Date TEXT, Region TEXT)')

# Import customer data to SQLite3

print('Import customer_data to SQLite3 ...')

with open(customer_data_file, 'r') as fhand:
    # Skip the header line
    next(fhand)
    num_customer = 0

    for line in fhand:
        num_customer = num_customer + 1
        print(num_customer)
        customer_data = line.split('\t')
        customer_ID = customer_data[0].strip()
        name = customer_data[1].strip()
        gender = customer_data[2].strip()
        ID = customer_data[3].strip()
        passport_ID = customer_data[4].strip()
        phone_number = customer_data[5].strip()
        project_IDs = customer_data[6].strip('"').split(',')
        expenses = customer_data[7].strip('"').split(',')
        spouse_IDs = customer_data[8].strip('"').split(',')
        children_IDs = customer_data[9].strip('"').split(',')
        relatives_IDs = customer_data[10].strip('"').split(',')
        friends_IDs = customer_data[11].strip('"').split(',')
        notes = customer_data[12].strip()

        # Calculate age
        if len(ID) == 18:
            age = current_year - int(ID[6:10])
        else:
            age = ''

        # Insert into Customer_Data table
        cur.execute('INSERT INTO Customer_Data (Customer_ID, Name, Gender, Age, ID, Passport_ID, Phone_Number, Notes) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', (int(customer_ID), str(name), str(gender), str(age), str(ID), str(passport_ID), str(phone_number), str(notes)))

        # Insert into Spouse_Relation table if feasible
        if len(spouse_IDs) > 0:
            for spouse_ID in spouse_IDs:
                if len(spouse_ID.strip()) > 0:
                    cur.execute('INSERT INTO Spouse_Relation (Customer_ID, Spouse_ID) VALUES (?, ?)', (int(customer_ID), int(spouse_ID)))

        # Insert into Children_Relation table if feasible
        if len(children_IDs) > 0:
            for children_ID in children_IDs:
                if len(children_ID.strip()) > 0:
                    cur.execute('INSERT INTO Children_Relation (Customer_ID, Children_ID) VALUES (?, ?)', (int(customer_ID), int(children_ID)))

        # Insert into Relatives_Relation table if feasible
        if len(relatives_IDs) > 0:
            for relatives_ID in relatives_IDs:
                if len(relatives_ID.strip()) > 0:
                    cur.execute('INSERT INTO Relatives_Relation (Customer_ID, Relatives_ID) VALUES (?, ?)', (int(customer_ID), int(relatives_ID)))


        # Insert into Friends_Relation table if feasible
        if len(friends_IDs) > 0:
            for friends_ID in friends_IDs:
                if len(friends_ID.strip()) > 0:
                    cur.execute('INSERT INTO Friends_Relation (Customer_ID, Friends_ID) VALUES (?, ?)', (int(customer_ID), int(friends_ID)))


        # Insert into Project_Participants table if feasible
        if len(project_IDs) > 0:
            for project_ID, expense in zip(project_IDs, expenses):
                if len(project_ID.strip()) > 0:
                    cur.execute('INSERT INTO Project_Participants (Customer_ID, Project_ID, Expense) VALUES (?, ?, ?)', (int(customer_ID), int(project_ID), int(expense)))

        # Save customer data to hard-drive routinely 
        if(num_customer % 100 == 0):
            conn.commit()
        
    conn.commit()

print('customer_data imported.')

# Import project data to SQLite3

print('Import project_data to SQLite3 ...')


with open(project_data_file, 'r') as fhand:
    # Skip the header line
    next(fhand)
    num_project = 0

    for line in fhand:
        num_project = num_project + 1
        print(num_project)
        project_data = line.split('\t')

        project_ID = project_data[0].strip()
        project_name = project_data[1].strip()
        price = project_data[2].strip()
        size = project_data[3].strip()
        date = project_data[4].strip()
        region = project_data[5].strip()

        # Insert into Project_Data table if feasible
        cur.execute('INSERT INTO Project_Data (Project_ID, Project_Name, Price, Size, Date, Region) VALUES (?, ?, ?, ?, ?, ?)', (int(project_ID), str(project_name), int(price), int(size), str(date), str(region)))

        # Save customer data to hard-drive routinely 
        if(num_project % 100 == 0):
            conn.commit()
        
    conn.commit()

print('project_data imported.')