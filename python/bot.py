import discord
from discord.ext import commands
import random

import os

from dotenv import load_dotenv
load_dotenv()

print("Bot is waking up...")

token = os.environ.get("DISCORD_TOKEN")
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix = "!", intents = intents)

@bot.event
async def on_ready():
    print(f"Logged on as {bot.user.name}")
    await bot.tree.sync()

@bot.tree.command(name = "roll", description = "Roll a dice!")
async def roll(interaction: discord.Interaction, roll: str = "d20"):
    await interaction.response.send_message("placeholder")

@bot.tree.command(name = "avatar", description = "Get users avatar")
async def avatar(interaction: discord.Interaction, member: discord.Member = None):
    await interaction.response.send_message(member.display_avatar)

bot.run(token)