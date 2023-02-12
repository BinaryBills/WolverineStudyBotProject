#Author: BinaryBills
#Creation Date: February 1, 2023
#Date Modified: February 11, 2023
#Purpose:
import discord
from discord.ext import commands
from discord import app_commands
from discord.app_commands import AppCommandError
import asyncio
import datetime

async def is_owner(interaction: discord.Interaction, member: discord.Member):
        if member.id == interaction.guild.owner_id:
            return True
        return False
    
class mod(commands.Cog):
    def __init__(self,client):
        self.client = client
        
    @app_commands.checks.has_permissions(manage_messages=True)
    @app_commands.checks.bot_has_permissions(manage_messages = True)
    @app_commands.command(name = "clear", description = "Clears a specified amount of messages")
    async def clear(self, interaction: discord.Interaction, amount : int):
     await interaction.response.defer(ephemeral = True)  
     await interaction.channel.purge(limit=amount)   
     await interaction.followup.send(f"{interaction.user.mention}, the previous **{amount} messages** have been removed!")
          
    @app_commands.checks.has_permissions(kick_members=True)
    @app_commands.checks.bot_has_permissions(kick_members = True)
    @app_commands.command(name = "kick", description = "Kicks a user")
    async def kick(self, interaction: discord.Interaction, member:discord.Member, reason:str):
          temp = member
          if await is_owner(interaction,member) == False:
           await interaction.guild.kick(member)
           await interaction.response.send_message(f"{temp.mention} has been kicked! Reason: {reason}!")
          else:
              await interaction.response.send_message("User specified is a privileged user!")
         
    @app_commands.checks.has_permissions(ban_members=True)
    @app_commands.checks.bot_has_permissions(ban_members = True)
    @app_commands.command(name = "ban", description = "Bans a user")
    async def ban(self, interaction: discord.Interaction, member:discord.Member, reason:str):
          temp = member
          if await is_owner(interaction,member) == False:
           await interaction.guild.ban(member)
           await interaction.response.send_message(f"{temp.mention} has been banned! Reason: {reason}!")
          else:
              await interaction.response.send_message("User specified is a privileged user!")
    
    @app_commands.checks.has_permissions(manage_messages=True)
    @app_commands.checks.bot_has_permissions(manage_messages=True)
    @app_commands.checks.bot_has_permissions(manage_roles=True)
    @app_commands.checks.bot_has_permissions(moderate_members=True)
    @app_commands.command(name="mute", description="Mutes a user")
    async def mute(self, interaction: discord.Interaction, member: discord.Member, seconds: int = 0, minutes: int = 0, hours: int = 0, days: int = 0, reason: str = None):
       #Make it so users cannot put in a time longer than 28 days later on
       if await is_owner(interaction,member) == True:
            await interaction.response.send_message("User specified is a priviledged user!")
       duration = datetime.timedelta(seconds=seconds, minutes=minutes, hours= hours, days=days)
       await member.timeout(duration, reason=reason)
       await interaction.response.send_message(f'{member.mention} was timeouted until for {duration}', ephemeral=True)
        
    #all errors will be handled here 
    async def cog_app_command_error(self, interaction: discord.Interaction, error: AppCommandError):
        print("This error was handled!")
        await interaction.response.send_message(f"Sorry {interaction.user.mention}, but you or the bot lack the permissions to access this command! An error of another type could have also occurred!")
              
async def setup(client):
    await client.add_cog(mod(client))