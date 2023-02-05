#Author: BinaryBills
#Creation Date: February 1, 2023
#Date Modified: February 5, 2023
#Purpose:
import discord
from discord.ext import commands
from discord import app_commands
from discord.app_commands import AppCommandError

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
          await interaction.channel.purge(limit=amount)
          await interaction.response.defer(ephemeral = True)
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
              
    
    #all errors will be handled here 
    async def cog_app_command_error(self, interaction: discord.Interaction, error: AppCommandError):
        print("This error was handled!")
        await interaction.response.send_message(f"Sorry {interaction.user.mention}, but you lack the permissions to access this command!")
              

async def setup(client):
    await client.add_cog(mod(client))
