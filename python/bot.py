import discord
from discord.ext import commands
from diceFunctions import DiceMachine

import os

from dotenv import load_dotenv
load_dotenv()

print("Bot is waking up...")

token = os.environ.get("DISCORD_TOKEN")
intents = discord.Intents.default()
intents.presences = True
intents.message_content = True
intents.members = True
activity = discord.Activity(type = discord.ActivityType.listening, name = "Marching Cadence")
bot = commands.Bot(command_prefix = "!", activity = activity, intents = intents)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Logged on as {bot.user.name}")

@bot.event
async def on_member_update(before, after):
    if after.nick != before.nick:
        file_path = os.path.join("nicknames", after.name + ".txt")
        with open(file_path, "a") as file:
            file.write(after.nick + "\n")

@bot.tree.command(name = "get_nicknames", description = "Displays all stored nicknames for a user")
async def get_nicknames(interaction: discord.Interaction):
    file_path = os.path.join("nicknames", interaction.user.name + ".txt")
    file_contents = "```"
    with open(file_path, "r") as file:
        file_contents += file.read()
    await interaction.response.send_message(file_contents + "```")

@bot.tree.command(name = "roll", description = "Roll a dice!")
async def roll(interaction: discord.Interaction, roll: str = "d20"):
    dm = DiceMachine(roll)
    dm.roll()
    await interaction.response.send_message(dm.roll_to_string())

@bot.tree.command(name = "avatar", description = "Get users avatar")
async def avatar(interaction: discord.Interaction, member: discord.Member = None):
    if member is not None:
        await interaction.response.send_message(member.display_avatar)
    else:
        await interaction.response.send_message("No member specified")

bot.run(token)