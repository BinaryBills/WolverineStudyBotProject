#Author: BinaryBills
#Creation Date: January 17, 2023
#Date Modified: January 18, 2023
#Purpose: This file's responsibility is to add users to the database and measure their engagement in a server.

import discord
from discord import app_commands
from discord.ext import commands
import platform
from config import settings
from config import sqlServer
import mysql.connector
import random
from easy_pil import *

async def userCard(row, author, guild):
         try:
          levelStats = list(row)
          level = int(levelStats[1])
          xp = int(levelStats[2])
         except TypeError:
             level = 0
             xp = 0
         
         userCard = {
             "name": f"{author}",
             "xp" : xp,
             "level" : level,
             "next_level_xp": 100,
             "percentage": xp,
            }
             
         #reaches
         background = Editor(Canvas((900,300), color = "#00294e"))
         profile_picture = await load_image_async(str(author.avatar.url))
         profile = Editor(profile_picture).resize((150,150)).circle_image()
         poppins = Font.poppins(size=40)
         poppins_small = Font.poppins(size=30)
         
         #reaches
         card_right_shape = [(600,0), (750,300), (900,300), (900,0)]
         background.polygon(card_right_shape, color="#f2c514")
         background.paste(profile, (30,30))
       
         
         #BAR
         background.rectangle( (30,220), width = 650, height = 40, color = "#FFFFFF" )
         print("does it ever reach here")
         background.bar( (30,220), max_width=650, height=40, percentage = userCard["percentage"], color = "#282828", radius=0)
         background.text( (200,40), userCard["name"], font=poppins, color = "#f2c514")
         
        
         
         background.rectangle( (200,100), width = 350, height=2, fill = "#f2c514")
         
         background.text(
             (200,130), 
             f"Level - {userCard['level']} | XP - {userCard['xp']}/{userCard['next_level_xp']}",
             font = poppins_small,
             color = "#f2c514",
         )
        
         file = discord.File(fp=background.image_bytes, filename = "levelcard.png")
         return file
    

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
             file = await userCard(row, author, guild)
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
         file = await userCard(row, author, guild)
         await interaction.response.send_message(file=file)
       
             
         
        
        
                     
        
async def setup(client):
    await client.add_cog(userSystem(client))
    
