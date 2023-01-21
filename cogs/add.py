#Author: BinaryBills
#Creation Date: December 25, 2022
#Date Modified: December 25, 2022
#Purpose:

import discord
from discord.ext import commands
from discord import app_commands
from discord import ui

class myModal(ui.Modal, title= "Upload a Study Resource"):
    field1 = ui.TextInput(label="Enter the Course:", placeholder = "CIS, IMSE, GEOL,...", style=discord.TextStyle.short)
    field2 = ui.TextInput(label="Enter the Course Number:", placeholder = "150,200, 350...", style=discord.TextStyle.short)
    field3 = ui.TextInput(label="Enter the Topic:", placeholder = "Recursion, Theory of forms,Tension force...   ", style=discord.TextStyle.short)
    field4 = ui.TextInput(label="Enter the link to the resource:", placeholder = " https://www.youtube.com/watch?v=4agL-MQq05E", style=discord.TextStyle.short)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"Hello, **{self.field1}**")

class add(commands.Cog):
    def __init__(self,client):
        self.client = client

    @app_commands.command(name = "add", description = "Adds a study resource to the WolverineStudyBot database!")
    async def add(self, interaction: discord.Interaction):
        await interaction.response.send_modal(myModal())

async def setup(client):
    await client.add_cog(add(client))
