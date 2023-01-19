#Author: BinaryBills
#Creation Date: January 17, 2022
#Date Modified: January 18, 2022
#Purpose: This file's responsibility is to add users to the database and measure their engagement in a server.

import discord
from discord import app_commands
from discord.ext import commands
import platform
from config import settings
from config import sqlServer
import mysql.connector
import random
import easy_pil


class userSystem(commands.Cog):
    def __init__(self,client):
        self.client = client
     
    @commands.Cog.listener()
    async def on_message(self,message):
        if message.author.bot:
            return
        author = message.author
        guild = message.guild
        row = await sqlServer.getSpecificRow(settings.conn, "discord_ID", author.id, "levels")
      
        if (row == None):
         """User was not found so we add them to our database"""
         sql = "INSERT IGNORE INTO levels (discord_ID, level, xp, guild, global_ban_status) VALUES ({}, {}, {}, {}, {})".format(author.id, 0, 0, guild.id, 0)
         await sqlServer.mysqli_user_query(settings.conn, sql)
        else:
         """User was found"""
         try:
             levelStats = list(row)
             level = int(levelStats[1])
             xp = int(levelStats[2])
             print(level,xp)
         except TypeError:
             level = 0
             xp = 0
             
         if level < 5:
             xp += random.randint(1,3)
             print(xp)
             await sqlServer.mysqli_user_query(settings.conn, "UPDATE levels SET xp = {} WHERE discord_ID = {} AND guild = {}".format(xp,author.id,guild.id))
         else:
             rand = random.randint(1, (level/4))
             if rand == 1:
                 xp += random.randint(1,3)
                 await sqlServer.mysqli_user_query(settings.conn, "UPDATE levels SET xp = {} WHERE discord_ID = {} AND guild = {}".format(xp,author.id,guild.id))
        
         if xp >= 100: 
             level += 1
             await sqlServer.mysqli_user_query(settings.conn, "UPDATE levels SET level = {} WHERE discord_ID = {} AND guild = {}".format(level,author.id,guild.id))
             await sqlServer.mysqli_user_query(settings.conn, "UPDATE levels SET xp = {} WHERE discord_ID = {} AND guild = {}".format(0,author.id,guild.id))
             await message.channel.send(f"{author.mention} has leveled up to level **{level}**!")
             
    @app_commands.command(name = "lvl", description = "Check your level in the guild!")
    async def level(self,interaction: discord.Interaction):
        author = interaction.user
        guild = interaction.guild.id
        row = await sqlServer.getSpecificRow(settings.conn, "discord_ID", author.id, "levels")
        
        if (row == None):
         """User was not found so we add them to our database"""
         sql = "INSERT IGNORE INTO levels (discord_ID, level, xp, guild, global_ban_status) VALUES ({}, {}, {}, {}, {})".format(author.id, 0, 0, guild.id, 0)
         await sqlServer.mysqli_user_query(settings.conn, sql)
        else:
         """User was found"""
         em = discord.Embed(title=f"{author}'s Level", description=f"Level: '{row[1]}'\nXP: '{row[2]}'")
         await interaction.response.send_message(embed=em)
        
        
                     
        
async def setup(client):
    await client.add_cog(userSystem(client))
    
