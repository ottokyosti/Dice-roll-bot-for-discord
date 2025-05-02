import yt_dlp as youtube_dl
import discord
from discord import FFmpegPCMAudio
from discord.ext import commands
from elevenlabs import VoiceSettings, save, play
from elevenlabs.client import ElevenLabs
from datetime import date
from diceFunctions import DiceMachine
from getVoiceSettings import get_voice_settings
from db_query import queryHelper

import os
import asyncio
import random

from dotenv import load_dotenv
load_dotenv()

print("Bot is waking up...")

token = os.environ.get("DISCORD_TOKEN")
intents = discord.Intents.default()
intents.presences = True
intents.message_content = True
intents.members = True
activity = discord.Activity(type = discord.ActivityType.listening, name = "Ghost")
bot = commands.Bot(command_prefix = "!", activity = activity, intents = intents)

elevenlabs_client = ElevenLabs(
    api_key = os.environ.get("ELEVENLABS_API_KEY"),
    timeout = 120
)

@bot.event
async def on_ready():
    print(f"Logged on as {bot.user.name}")

@bot.event
async def on_member_update(before: discord.Member, after: discord.Member):
    if after.nick != before.nick:
        today = date.today()
        file_path = os.path.join("nicknames", after.name + ".txt")
        with open(file_path, "a") as file:
            file.write(f"[{today.strftime('%d/%m/%Y')}] {after.nick}\n")

@bot.event
async def on_voice_state_update(member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
    if not member.bot and before.channel is None and after.channel:
        if len(after.channel.members) <= 1:
            return
        # fiftyFifty = random.randint(0, 1)
        # if (fiftyFifty == 0):
        #     audio = elevenlabs_client.generate(
        #         text = f"Jaaahas, kukas se siellä, {member.nick}, tervetuloa masentumaan kanavalle {after.channel.name}!",
        #         voice = "Roope",
        #         model = "eleven_multilingual_v2",
        #         voice_settings = get_voice_settings("Roope")
        #     )

        #     save(audio, "output.mp3")

        #     voice_client = await after.channel.connect()
        #     if voice_client.is_playing():
        #         voice_client.stop()
        #     voice_client.play(FFmpegPCMAudio("output.mp3"))
        #     while voice_client.is_playing():
        #         await asyncio.sleep(0.5)
        #     await voice_client.disconnect()
        #     os.remove("output.mp3")
        # else:
        file = await queryHelper()
        voice_client = await after.channel.connect()
        if voice_client.is_playing():
            voice_client.stop()
        voice_client.play(FFmpegPCMAudio(file))
        while voice_client.is_playing():
            await asyncio.sleep(0.5)
        await voice_client.disconnect()

@bot.command(name = "sync")
async def sync_commands(ctx: commands.Context):
    await bot.tree.sync()
    message = await ctx.send(f"Bot commands synced")
    await asyncio.sleep(3)
    await message.delete()
    await ctx.message.delete()


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

@bot.hybrid_command(name = "viisaus", description = "Dispenses wisdom from the mouth of Niilo22")
async def viisaus(ctx: commands.Context):
    if not ctx.author.voice or not ctx.author.voice.channel:
        await ctx.send(f"You must be in a voice channel to use this command!")
        return
    
    file = await queryHelper()
    voice_channel = ctx.author.voice.channel
    voice_client = await voice_channel.connect()
    if not voice_client.is_playing():
        await ctx.send(file = discord.File("media/img/peukku500.png"), delete_after = 5, silent = True)
        voice_client.play(FFmpegPCMAudio(file))
        while voice_client.is_playing():
            await asyncio.sleep(0.5)
    else:
        await ctx.send("I'm already playing!")
    await voice_client.disconnect()

@bot.hybrid_command(name = "mimir", description = "Give your homies a good night!")
async def mimir(ctx: commands.Context):
    if not ctx.author.voice or not ctx.author.voice.channel:
        await ctx.send(f"You must be in a voice channel to use this command!")
        return
    
    voice_channel = ctx.author.voice.channel
    voice_client = await voice_channel.connect()
    if not voice_client.is_playing():
        file_path_audio = os.path.join("media", "audio", "envoiauttaa.mp3")
        await ctx.send(file = discord.File("media/img/niilo_thumb.png"), silent = True)
        voice_client.play(FFmpegPCMAudio(file_path_audio))
        while voice_client.is_playing():
            await asyncio.sleep(0.5)
    else:
        await ctx.send("I'm already playing!")
    await voice_client.disconnect()     
        
@bot.hybrid_command(name = "say", description = "Write something and let the bot say it")
async def say(ctx: commands.Context, voice: str, msg: str):
    voice_settings = get_voice_settings(voice)
    if voice_settings is None:
        await ctx.send(f"Cannot find voice by the name of {voice}")
        return
    
    if ctx.author.voice and ctx.author.voice.channel:
        await ctx.defer()
        audio = elevenlabs_client.generate(
            text = msg,
            voice = voice,
            model = "eleven_multilingual_v2",
            voice_settings = voice_settings
        )

        save(audio, "output.mp3")

        voice_channel = ctx.author.voice.channel
        voice_client = await voice_channel.connect()
        if not voice_client.is_playing():
            voice_client.play(FFmpegPCMAudio("output.mp3"))
            while voice_client.is_playing():
                await asyncio.sleep(0.5)
            await ctx.send(f"{voice}: {msg}")
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
            file_path_audio = os.path.join("media", "audio", "chipi.mp3")
            sent_message = await ctx.send(file = discord.File("media/img/chipi-chipi-chapa-chapa.gif"))
            voice_client.play(FFmpegPCMAudio(file_path_audio))
            while voice_client.is_playing():
                await asyncio.sleep(0.5)
            await sent_message.delete()
        else:
            await ctx.send("I'm already playing!")
        await voice_client.disconnect() 
    else:
        await ctx.send("You must be in a voice channel to use this command!")

@bot.hybrid_command(name = "play", description = "Play a sound bite from Youtube")
async def play(ctx: commands.Context, url: str, volume: int = 75):
    if ctx.author.voice and ctx.author.voice.channel:
        await ctx.defer()
        voice_channel = ctx.author.voice.channel

        ydl_opts = {
            "format": "bestaudio/best",
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192"
            }],
            "outtmpl": "media/audio/%(title)s.%(ext)s",
            "noplaylist": True
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download = True)
            duration = info.get("duration", 0)
            filename = ydl.prepare_filename(info).replace(".webm", ".mp3").replace(".m4a", ".mp3")

        if (duration < 120):
            voice_client = await voice_channel.connect()
            if not voice_client.is_playing():
                await ctx.send(f"Playing audio at {volume}% volume")
                ffmpeg_options = {
                    "options": f"-filter:a 'volume={volume / 100}'"
                }
                voice_client.play(FFmpegPCMAudio(filename, **ffmpeg_options))
                while voice_client.is_playing():
                    await asyncio.sleep(0.5)
            else:
                await ctx.send("I'm already playing!")
            await voice_client.disconnect()
            await ctx.send(url)
        else:
            await ctx.send("Video is too long! Must be under 2 minutes")
        os.remove(filename)
    else:
        await ctx.send("You must be in a voice channel to use this command!")

@bot.hybrid_command(name = "stop", description = "Stop the bot from playing audio")
async def stop(ctx: commands.Context):
    if (ctx.voice_client):
        if (ctx.voice_client.is_playing()):
            ctx.voice_client.stop()
            await ctx.send("Stopped playing audio")
        else:
            await ctx.send("I'm not playing audio...")
    else:
        await ctx.send("I'm not connected to a voice channel...")

bot.run(token)