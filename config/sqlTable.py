#Author: BinaryBills
#Creation Date: January 8, 2023
#Date Modified: March 17, 2023
#Purpose: Declaration of SQL Tables for the database and helper functions to make using the tables minimal work.


#redesign tables

departmentsTable = "CREATE TABLE IF NOT EXISTS departments (id SERIAL PRIMARY KEY, department_code VARCHAR(10) NOT NULL UNIQUE)"
coursesTable = "CREATE TABLE IF NOT EXISTS courses (id SERIAL PRIMARY KEY, department_id INTEGER NOT NULL, course_number VARCHAR(10) NOT NULL, UNIQUE (department_id, course_number), FOREIGN KEY (department_id) REFERENCES departments(id))"
academicResTable = "CREATE TABLE IF NOT EXISTS academic_resources ( id SERIAL PRIMARY KEY, course_id INTEGER NOT NULL, resource_name VARCHAR(255) NOT NULL, resource_link TEXT NOT NULL, uploader_id VARCHAR(255) NOT NULL, upload_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY (course_id) REFERENCES courses(id))"










guildsTable = "CREATE TABLE IF NOT EXISTS Guilds(guildID VARCHAR(256) NOT NULL PRIMARY KEY,guildOwnerID VARCHAR(256) NOT NULL)"
guildConfigTable = "CREATE TABLE IF NOT EXISTS GuildConfig(guildID VARCHAR(256) NOT NULL PRIMARY KEY,modLogID VARCHAR(256) NOT NULL,xpLogID VARCHAR(256) NOT NULL)"
usersTable = "CREATE TABLE IF NOT EXISTS users (discord_ID varchar(256) PRIMARY KEY NOT NULL, global_ban_status varchar(1) NOT NULL)"
levels = "CREATE TABLE IF NOT EXISTS levels (discord_ID varchar(256) PRIMARY KEY NOT NULL, level INTEGER, xp INTEGER, guild varchar(256), global_ban_status varchar(1) NOT NULL)"
GuildMemberExperience = "CREATE TABLE IF NOT EXISTS GuildMemberExperience(guildID VARCHAR(256) NOT NULL, memberID VARCHAR(256) NOT NULL, currLvl SMALLINT NOT NULL DEFAULT 1, xp INT NOT NULL DEFAULT 1, PRIMARY KEY (guildID, memberID)"

