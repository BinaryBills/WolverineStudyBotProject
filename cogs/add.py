# Author: BinaryBills
# Creation Date: December 25, 2023
# Date Modified: March 17, 2023
# Purpose:

import discord
from discord.ext import commands
from discord import app_commands
from discord import ui
from config import settings
from config import sqlServer
from config.sqlServer import department_exists, course_exists

async def add_resource(course_id, resource_name, resource_link, uploader_id):
    
    #Check if the resource link already exists in the database
    query = f"SELECT * FROM academic_resources WHERE resource_link = '{resource_link}'"
    cursor = settings.conn.cursor()
    cursor.execute(query)
    result = cursor.fetchone()

    # If the resource link already exists, return False
    if result:
        return False

    # Otherwise, add the resource and return True
    try:
        query = f"""INSERT INTO academic_resources (course_id, resource_name, resource_link, uploader_id) VALUES ({course_id}, '{resource_name}', '{resource_link}', '{uploader_id}')"""
        sqlServer.execute_query(settings.conn, query)
        settings.conn.commit()
        sqlServer.print_table_contents(settings.conn, "academic_resources")
        return True
    except Exception as e:
        print(f"Error adding resource: {e}")
        return False



class myModal(ui.Modal, title="Upload a Study Resource"):
    field1 = ui.TextInput(label="Enter the Course:", placeholder="CIS, IMSE, GEOL,...", style=discord.TextStyle.short)
    field2 = ui.TextInput(label="Enter the Course Number:", placeholder="150,200, 350...", style=discord.TextStyle.short)
    field3 = ui.TextInput(label="Enter the Topic:", placeholder="Recursion, Theory of forms, Tension force...   ", style=discord.TextStyle.short)
    field4 = ui.TextInput(label="Enter the link to the resource:", placeholder="https://www.youtube.com/watch?v=4agL-MQq05E", style=discord.TextStyle.short)

    async def on_submit(self, interaction: discord.Interaction):
        """
        Processes the user's input and adds the resource to the database if the input is valid.
        """
        try:
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
                    added = await add_resource(course_id, resource_name, link, uploader_id)
                
                    if added:
                     await interaction.response.send_message(f"Resource '{resource_name}' added for {course_code} {course_number}: {resource_name}")
                    else:
                     await interaction.response.send_message(f"The resource link already exists in the database.")
                else:
                    await interaction.response.send_message(f"An error occurred while adding the resource")
        except Exception as e:
            print(f"Error in on_submit: {e}")
            await interaction.response.send_message("An error occurred while processing your request. Please try again later.")

class Add(commands.Cog):
    """
    A cog that defines the "add" command for the bot.
    """
    def __init__(self, client):
        self.client = client

    @app_commands.command(name="add", description="Adds a study resource to the WolverineStudyBot database!")
    async def add(self, interaction: discord.Interaction):
        await interaction.response.send_modal(myModal())

async def setup(client):
    await client.add_cog(Add(client))
