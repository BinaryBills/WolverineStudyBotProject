#Author: BinaryBills
#Creation Date: January 15, 2022
#Date Modified: January 18, 2022
#Purpose: The Remind command allows users to request the bot to message them at a specified time with a specific message. This functionality will help students plan study sessions.

import discord
from discord.ext import commands
from discord import app_commands
import asyncio

async def isUnitValid(unit):
     """Checks if the unit entered by the user is valid by comparing it with entries in the units list"""
     units = ['s', 'sec', 'secs', 'second', 'seconds', 'm', 'min', 'mins', 'minute', 'minutes','h', 'hr', 'hour', 'hours', 'd', 'day', 'days']
     if unit in units:
         return True
     else:
         return False

async def convertUnitToSeconds(unit, time):
    """If the unit entered by the user is valid, we convert it to seconds. 
    If the time entered by the user is valid and postive, we multiply it with our 
    converted unit to find the time we need to wait.
    """
    if (await isUnitValid(unit) == False):
        return -1
    time_units = {'s': 1, 'sec':1, 'secs':1, 'second':1, 'seconds':1, 'm':60, 'min':60, 'mins':60, 'minute':60, 'minutes':60,'h':3600, 'hr':3600, 'hour':3600, 'hours':3600, 'd':86400, 'day':86400, 'days':86400}
    try:
     val = int(time)  
    except:
     return -2
    return val * time_units[unit]


class remind(commands.Cog):
    def __init__(self, client):
        self.client = client
        
   
    @app_commands.command(name = "remind", description = "Set a reminder using WolverineStudyBot!")
    async def remind(self, interaction: discord.Interaction, time : str,*, unit: str, task : str):

        unit = unit.lower()
        converted_time = await convertUnitToSeconds(unit, time)

        if converted_time == -1 or time <=0:
            await interaction.response.send_message("You didn't answer the time correctly")
            return

        if converted_time == -2:
            await interaction.response.send_message("The time must be an integer")
            return
        
        if (int(converted_time) > 2419000):   
         await interaction.response.send_message("Time cannot be more than 28 days!")

        @commands.Cog.listener()
        async def setReminder(message, channel, user, converted_time, task):  
            """Discord Interactions are only active for 15 minutes so we convert it into a message
            This circumvents the issue."""
            print("Reminder noticed")
            for x in range(0, converted_time+1):
             await asyncio.sleep(1)
             #print(x)
            await channel.send(f"{user.mention} your reminder for **{task}** has finished!")
            
        await interaction.response.send_message(f'Started reminder for **{task}** and will last **{time} {unit}** .')
        print(f'{self.client.user} has set a reminder!')
        await setReminder(interaction.message, interaction.channel, interaction.user, converted_time, task)
        
       
        
      

        
        
        
        
    
async def setup(client):
      await client.add_cog(remind(client))