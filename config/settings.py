#Author: BinaryBills
#Creation Date: January 8, 2023
#Date Modified: March 17, 2023
#Purpose: This file is responsible for loading the bot's sensitive data,
#connecting to the targeted SQL server, and adding all the tables to 
#the database needed for the bot to function.

import os
from config import sqlServer
from config import sqlTable
from dotenv import load_dotenv
from datetime import datetime
from pytz import timezone
import asyncio

############################################
#         Figuring out time                #
############################################
def getTime():
    tz = timezone('EST')
    return str(datetime.now(tz)) 

############################################
#        Loading secret data               #
############################################
"""Loads data from .env to get the discord bot API key and SQL server credentials"""
load_dotenv()
TOKEN = os.getenv("DISCORD_API_TOKEN")
HOSTNAME = str(os.getenv("HOST_NAME"))
USERNAME = str(os.getenv("USER_NAME"))
PASSWD = str(os.getenv("PASSWORD_NAME"))
DB = str(os.getenv("DATABASE_NAME"))
serverInfo = [HOSTNAME, USERNAME, PASSWD, DB]

############################################
#      Connecting to server                #
############################################
"""Connects and creates database if it does not already exist"""
conn = sqlServer.connectToServer(HOSTNAME, USERNAME, PASSWD)
sqlServer.mysqli_query(conn, f"CREATE DATABASE IF NOT EXISTS {DB}" )
conn = sqlServer.connectToDatabase(HOSTNAME, USERNAME, PASSWD, DB)

############################################
#      Creating the SQL Tables             #
############################################
"""Initializing SQL TABLES"""
sqlServer.mysqli_query(conn, sqlTable.departmentsTable)
sqlServer.mysqli_query(conn, sqlTable.coursesTable)
sqlServer.mysqli_query(conn, sqlTable.academicResTable)
sqlServer.mysqli_query(conn, sqlTable.levels)

############################################
#    Populating Course & Departments       #
############################################
"""Initializing Course & Department Table with numbers"""
department_list = ['CIS','ENGR']
sqlServer.initialize_departments(conn, department_list)
sqlServer.initialize_courses(conn, department_list)

sqlServer.mysqli_query(conn, sqlTable.usersTable)
sqlServer.mysqli_query(conn, sqlTable.guildConfigTable)
sqlServer.mysqli_query(conn, sqlTable.guildsTable)


