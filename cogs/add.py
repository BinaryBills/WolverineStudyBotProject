#Author: BinaryBills
#Creation Date: December 25, 2023
#Date Modified: March 17, 2023
#Purpose:

import discord
from discord.ext import commands
from discord import app_commands
from discord import ui
from config import sqlServer
from config import settings

async def add_resource(course_id, resource_name, resource_link, uploader_id):
   query = f"""INSERT INTO academic_resources (course_id, resource_name, resource_link, uploader_id) VALUES ({course_id}, '{resource_name}', '{resource_link}', '{uploader_id}')"""
   sqlServer.mysqli_query(settings.conn, query)
    
async def department_exists(connection, department_code):
    query = f"SELECT COUNT(*) FROM departments WHERE department_code = '{department_code}'"
    cursor = connection.cursor()
    cursor.execute(query)
    count = cursor.fetchone()[0]
    return count > 0

async def course_exists(connection, department_code, course_number):
    query = f"""
        SELECT COUNT(*)
        FROM courses
        JOIN departments ON courses.department_id = departments.id
        WHERE departments.department_code = '{department_code}' AND courses.course_number = '{course_number}'
    """
    cursor = connection.cursor()
    cursor.execute(query)
    count = cursor.fetchone()[0]
    return count > 0
    

class myModal(ui.Modal, title= "Upload a Study Resource"):
    field1 = ui.TextInput(label="Enter the Course:", placeholder = "CIS, IMSE, GEOL,...", style=discord.TextStyle.short)
    field2 = ui.TextInput(label="Enter the Course Number:", placeholder = "150,200, 350...", style=discord.TextStyle.short)
    field3 = ui.TextInput(label="Enter the Topic:", placeholder = "Recursion, Theory of forms,Tension force...   ", style=discord.TextStyle.short)
    field4 = ui.TextInput(label="Enter the link to the resource:", placeholder = " https://www.youtube.com/watch?v=4agL-MQq05E", style=discord.TextStyle.short)


    async def on_submit(self, interaction: discord.Interaction):
        course_code = self.field1.value
        course_number = self.field2.value
        resource_name = self.field3.value
        link = self.field4.value
        uploader_id = interaction.user.id
        
        if not await department_exists(settings.conn, course_code):
            await interaction.response.send_message(f"Invalid department: {course_code}")
        elif not await course_exists(settings.conn, course_code, course_number):
            await interaction.response.send_message(f"Invalid course number: {course_number}")
        else:
            query = f"""
                SELECT courses.id
                FROM courses
                JOIN departments ON courses.department_id = departments.id
                WHERE departments.department_code = '{course_code}' AND courses.course_number = '{course_number}'
            """
            cursor = settings.conn.cursor()
            cursor.execute(query)
            course_id = cursor.fetchone()
            
            if course_id:
                course_id = course_id[0]
                await add_resource(course_id, resource_name, link, uploader_id)
                await interaction.response.send_message(f"Resource '{resource_name}' added for {course_code} {course_number}: {resource_name}")
            else:
                await interaction.response.send_message(f"An error occurred while adding the resource")


class Add(commands.Cog):
    def __init__(self,client):
        self.client = client

    @app_commands.command(name = "add", description = "Adds a study resource to the WolverineStudyBot database!")
    async def add(self, interaction: discord.Interaction):
        await interaction.response.send_modal(myModal())

async def setup(client):
    await client.add_cog(Add(client))
