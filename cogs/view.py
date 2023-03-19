import discord
from discord.ext import commands
from discord import app_commands
from discord import ui
from config import sqlServer
from config import settings
import asyncio

async def getCourse(row):
  #Get course id from academic resources then find its associated row in course first
  #From that course, extract its department and get its associated row in the department.
  #department[1] + " " + course[2]
  courseInfo = await sqlServer.getSpecificRow(settings.conn , "id", row[1], "courses")
  departmentInfo = await sqlServer.getSpecificRow(settings.conn , "id", courseInfo[1], "departments")
  return(str(" " + departmentInfo[1] + " " + courseInfo[2]))
    

class Paginator(ui.View):
    def __init__(self, data, timeout=900):
        super().__init__(timeout=timeout)
        self.data = data
        self.current_page = 0
        self.items_per_page = 5

    async def send_initial_message(self, interaction):
        try:
            await interaction.response.defer(ephemeral=True)
            self.message = await interaction.channel.send(
                embed=self.create_embed(self.get_current_page_data()), view=self
            )
            self.last_interaction = interaction
            asyncio.create_task(self.delete_message_after_timeout())
            return self.message
        except Exception as e:
            print(e)


    def create_embed(self, data):
        """Sets the embed layout for the table and each singular element listed in the table"""
        embed = discord.Embed(
            title=f"Resources Page {self.current_page + 1} / {len(self.data) // self.items_per_page + 1}",
            description="Here are the academic resources we found for you!:",
            color=0x303236,
        )

        for item in data:
            embed.add_field(
                name=item["resource_name"],
                value=f"Course:{item['course_info']}\nLink: {item['resource_link']}\nUploader ID: {item['uploader_id']}\nDate: {item['upload_date']}",
                inline=False,
            )
        return embed

    def get_current_page_data(self):
        start = self.current_page * self.items_per_page
        end = start + self.items_per_page
        return self.data[start:end]

    @ui.button(label="Previous", style=discord.ButtonStyle.primary, custom_id="previous_button", row=0)
    async def previous_page(self, interaction: discord.Interaction, button: discord.ui.Button):
        """This function allows the user to move one page backwards in the paginated table."""
        
        #If the current page is the first page, we go to the last page.
        #If the current page is not the first page, we move to the previous page.
        if self.current_page == 0:
            self.current_page = len(self.data) // self.items_per_page
        else:
            self.current_page -= 1
            
        try:
            await interaction.response.edit_message(embed=self.create_embed(self.get_current_page_data()), view=self)
        except discord.errors.NotFound:
            pass
        except Exception as e:
            print(e)

    @ui.button(label="Next", style=discord.ButtonStyle.primary, custom_id="next_button", row=0)
    async def next_page(self, interaction: discord.Interaction, button: discord.ui.Button):
        """This function allows the user to move one page forward in the paginated table."""
        
        #If the current page is the last page, we go to the first page.
        #If the current page is not the last page, we move forward one page. 
        if self.current_page == len(self.data) // self.items_per_page:
            self.current_page = 0
        else:
            self.current_page += 1
              
        try:
            await interaction.response.edit_message(embed=self.create_embed(self.get_current_page_data()), view=self)
        except discord.errors.NotFound:
            pass
        except Exception as e:
            print(e)
            
    async def delete_message_after_timeout(self):
        await asyncio.sleep(self.timeout)
        await self.delete_message()

    async def delete_message(self):
        try:
             await self.message.delete()
             await self.last_interaction.followup.send("The resource page has timed out.")
        except discord.errors.NotFound:
            pass
        except Exception as e:
            print(e)
           
    async def on_timeout(self):
        pass
        
        
class searchEngine(commands.Cog):
    def __init__(self, client):
        self.client = client

    @app_commands.command(name="view", description="View academic resources!")
    async def view(self, interaction: discord.Interaction, keywords: str = ""):
        try:
            # Grab correct information from the table
            cursor = settings.conn.cursor()
            
            query = """SELECT ar.id, ar.resource_name, d.department_code, c.course_number, ar.resource_link, ar.uploader_id, ar.upload_date
                       FROM academic_resources ar
                       INNER JOIN courses c ON ar.course_id = c.id
                       INNER JOIN departments d ON c.department_id = d.id"""
                       
                       
            params = []

            if keywords:
                query += " WHERE ar.resource_name LIKE %s"
                params = (f"%{keywords}%",)
            
            cursor.execute(query, params)
            data = cursor.fetchall()
            cursor.close()
        except Exception as e:
            print(e)
            await interaction.response.send_message("Error: Unable to fetch data from database.", ephemeral=True)
            return
        if not data:
            await interaction.response.send_message("No academic resources found.", ephemeral=True)
            return

        data_dict = [
            {
                 "resource_name": row[1],
                 "course_info": f"{row[2]} {row[3]}",
                 "resource_link": row[4],
                 "uploader_id": row[5],
                 "upload_date": row[6].strftime("%Y-%m-%d"),
            }
            for row in data
        ]

        paginator = Paginator(data_dict)
        try:
            await paginator.send_initial_message(interaction)
        except Exception as e:
            print(e)
            
async def setup(client):
    await client.add_cog(searchEngine(client))