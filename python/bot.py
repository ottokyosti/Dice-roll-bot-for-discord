import discord
from discord import FFmpegPCMAudio
from discord.ext import commands
from elevenlabs import VoiceSettings, save
from elevenlabs.client import ElevenLabs
from datetime import date
from diceFunctions import DiceMachine

import os
import asyncio

from dotenv import load_dotenv
load_dotenv()

print("Bot is waking up...")

token = os.environ.get("DISCORD_TOKEN")
intents = discord.Intents.default()
intents.presences = True
intents.message_content = True
intents.members = True
activity = discord.Activity(type = discord.ActivityType.listening, name = "Chipi Chipi Chapa Chapa")
bot = commands.Bot(command_prefix = "!", activity = activity, intents = intents)

elevenlabs_client = ElevenLabs(
    api_key = os.environ.get("ELEVENLABS_API_KEY")
)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Logged on as {bot.user.name}")

@bot.event
async def on_member_update(before, after):
    if after.nick != before.nick:
        today = date.today()
        file_path = os.path.join("nicknames", after.name + ".txt")
        with open(file_path, "a") as file:
            file.write(f"[{today.strftime('%d/%m/%Y')}] {after.nick}\n")

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

@bot.hybrid_command(name = "say", description = "Write something and let the bot say it")
async def say(ctx: commands.Context, msg: str):
    if ctx.author.voice and ctx.author.voice.channel:
        await ctx.defer()
        audio = elevenlabs_client.generate(
            text = msg,
            voice = "roope",
            model = "eleven_multilingual_v2",
            voice_settings = VoiceSettings(
                stability = 0.3,
                similarity_boost = 0.9,
                style = 0.75
            )
        )

        save(audio, "output.mp3")

        voice_channel = ctx.author.voice.channel
        voice_client = await voice_channel.connect()
        if not voice_client.is_playing():
            voice_client.play(FFmpegPCMAudio("output.mp3"))
            while voice_client.is_playing():
                await asyncio.sleep(1)
            await ctx.send(msg)
        else:
            await ctx.send("I'm already playing!")
        await voice_client.disconnect()
        os.remove("output.mp3")
    else:
        await ctx.send("You must be in a voice channel to use this command!")

@bot.hybrid_command(name = "chipichipi", description = "Chipi chipi chapa chapa")
async def chipi(ctx: commands.Context):
    if ctx.author.voice and ctx.author.voice.channel:
        await ctx.defer()
        voice_channel = ctx.author.voice.channel
        voice_client = await voice_channel.connect()

        if not voice_client.is_playing():
            with open("chipi-chipi-chapa-chapa.gif", "rb") as file:
                sent_message = await ctx.send(file = discord.File(file))
            voice_client.play(FFmpegPCMAudio("chipi.mp3"))
            while voice_client.is_playing():
                await asyncio.sleep(1)
        else:
            await ctx.send("I'm already playing!")
        
        await voice_client.disconnect()
        await sent_message.delete()
    else:
        await ctx.send("You must be in a voice channel to use this command!")

bot.run(token)