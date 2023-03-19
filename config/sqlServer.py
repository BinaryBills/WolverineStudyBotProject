#Author: BinaryBills
#Creation Date: January 8, 2023
#Date Modified: January 17, 2023
#Purpose: Functions used to open an active connection and send data to the Wamp server.

import mysql.connector
from mysql.connector import Error
from config import settings
from config import courseNumbers

def connectToServer(host_name, user_name, user_password):
    """
    Given a SQL server, it connects to it and accesses 
    its information. 
    Source: https://realpython.com/python-sql-libraries/#mysql_1
    """
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
        )
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")
        exit()
    return connection

def connectToDatabase(host_name, user_name, user_password, db_name):
    """
    Given a SQL server with a database specified by the user, 
    it connects to it and accesses its information. 
    Source: https://realpython.com/python-sql-libraries/#mysql_1
    """
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database = db_name
        )
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")
        exit()
    return connection

def mysqli_query(connection, query, params=None, cursor=None):
    """
    Given a SQL server and a SQL command, it sends a query to the server.
    """
    if cursor is None:
        cursor = connection.cursor()

    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        print(f"Command '{query}' processed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")
    
    return cursor
        
def initialize_departments(conn, default_departments):
    """Given a department code, it inserts it into the SQL department table"""
    try:
     for department in default_departments:
        mysqli_query(conn, f"INSERT IGNORE INTO departments (department_code) VALUES ('{department}');")
    except mysql.connector.Error as error:
          print(f"Error: {error}")
        
def initialize_courses(connection, department_list):
    # Insert courses if they don't already exist
    cursor = connection.cursor()

    for department_code in department_list:
        # Get the department_id for the given department_code
        dept_id_query = f"SELECT id FROM departments WHERE department_code = '{department_code}'"
        cursor = mysqli_query(connection, dept_id_query, cursor=cursor)
        department_id = cursor.fetchone()

        if department_id:
            department_id = department_id[0]
            course_numbers = courseNumbers.getCourseNumberList(department_code)

            for course_number in course_numbers:
                insert_query = f"""
                    INSERT IGNORE INTO courses (department_id, course_number)
                    VALUES ({department_id}, '{course_number}')
                """
                cursor = mysqli_query(connection, insert_query, cursor=cursor)

    # Commit the changes
    connection.commit()
   
async def mysqli_user_query(connection, query):
    """
    Given a SQL server and a SQL command, a user can send a query to the server.
    #Source: https://realpython.com/python-sql-libraries/#mysql_1
    """
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Command '{query}' processed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")

async def getSpecificRow(connection, primaryKey, input, table):
    """
    Gets an entire specified row given necessary data.
    """
    cursor = connection.cursor()
    try:
        query="SELECT * FROM {} WHERE {} = {}".format(table,primaryKey,input)
        cursor.execute(query)
        print("Command '{}' processed successfully".format(query))
        return cursor.fetchone()
    except Error as e:
        print(f"The error '{e}' occurred")
        

        



