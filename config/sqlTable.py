#Author: BinaryBills
#Creation Date: January 8, 2022
#Date Modified: January 17, 2022
#Purpose: Declaration of SQL Tables for the database and helper functions to make using the tables minimal work.


#redesign tables
guildsTable = "CREATE TABLE IF NOT EXISTS Guilds(guildID VARCHAR(256) NOT NULL PRIMARY KEY,guildOwnerID VARCHAR(256) NOT NULL)"
guildConfigTable = "CREATE TABLE IF NOT EXISTS GuildConfig(guildID VARCHAR(256) NOT NULL PRIMARY KEY,modLogID VARCHAR(256) NOT NULL,xpLogID VARCHAR(256) NOT NULL)"
usersTable = "CREATE TABLE IF NOT EXISTS users (discord_ID varchar(256) PRIMARY KEY NOT NULL, global_ban_status varchar(1) NOT NULL)"
levels = "CREATE TABLE IF NOT EXISTS levels (discord_ID varchar(256) PRIMARY KEY NOT NULL, level INTEGER, xp INTEGER, guild varchar(256), global_ban_status varchar(1) NOT NULL)"
GuildMemberExperience = "CREATE TABLE IF NOT EXISTS GuildMemberExperience(guildID VARCHAR(256) NOT NULL, memberID VARCHAR(256) NOT NULL, currLvl SMALLINT NOT NULL DEFAULT 1, xp INT NOT NULL DEFAULT 1, PRIMARY KEY (guildID, memberID)"

