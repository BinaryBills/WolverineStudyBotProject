import discord
from discord.ext import commands
from discord import app_commands
from discord import ui
from config import sqlServer
from config import settings


class Paginator(ui.View):
    def __init__(self, data, timeout=900):
        super().__init__(timeout=timeout)
        self.data = data
        self.current_page = 0
        self.items_per_page = 5

    async def send_initial_message(self, interaction):
        try:
            self.message = await interaction.response.send_message(
                embed=self.create_embed(self.get_current_page_data()), view=self, ephemeral=False
            )
            return self.message
        except Exception as e:
            print(e)

    def create_embed(self, data):
        embed = discord.Embed(
            title=f"Resources Page {self.current_page + 1} / {len(self.data) // self.items_per_page + 1}",
            description="Here are the test resources:",
            color=0x303236,
        )

        for item in data:
            embed.add_field(
                name=item["resource_name"],
                value=f"Link: {item['resource_link']}\nUploader ID: {item['uploader_id']}\nDate: {item['upload_date']}",
                inline=False,
            )
        return embed

    def get_current_page_data(self):
        start = self.current_page * self.items_per_page
        end = start + self.items_per_page
        return self.data[start:end]

    @ui.button(
        label="Previous", style=discord.ButtonStyle.primary, custom_id="previous_button", row=0
    )
    async def previous_page(self, button: discord.ui.Button, interaction: discord.Interaction):
        if self.current_page == 0:
            self.current_page = len(self.data) // self.items_per_page
        else:
            self.current_page -= 1
        try:
            await button.message.edit(embed=self.create_embed(self.get_current_page_data()), view=self)
        except discord.errors.NotFound:
            pass
        except Exception as e:
            print(e)

    @ui.button(label="Next", style=discord.ButtonStyle.primary, custom_id="next_button", row=0)
    async def next_page(self, button: discord.ui.Button, interaction: discord.Interaction):
        if self.current_page == len(self.data) // self.items_per_page:
            self.current_page = 0
        else:
            self.current_page += 1
        try:
            await button.message.edit(embed=self.create_embed(self.get_current_page_data()), view=self)
        except discord.errors.NotFound:
            pass
        except Exception as e:
            print(e)


class searchEngine(commands.Cog):
    def __init__(self, client):
        self.client = client

    @app_commands.command(name="view", description="View test resources!")
    async def view(self, interaction: discord.Interaction):
        # Test data
        data = [
            {
                "resource_name": f"Resource {i}",
                "resource_link": f"https://www.example.com/resource{i}",
                "uploader_id": f"User{i}",
                "upload_date": f"2023-03-17",
            }
            for i in range(1, 25)
        ]

        paginator = Paginator(data)
        try:
            await paginator.send_initial_message(interaction)
        except Exception as e:
            print(e)

async def setup(client):
    await client.add_cog(searchEngine(client))
