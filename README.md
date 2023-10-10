# Dice-roll-bot-for-discord

The Dice Roll Bot for Discord, initially developed primarily for rolling dice, has evolved into a versatile bot with various random (and funny, depending on the person) features. It allows you to roll dice and more within your Discord server. It supports any numbered dice used in DnD or any other tabletop.

## Features

- Roll various types of dice (e.g., d4, d6, d20, etc.).
- Roll multiple dice at once.
- Customize your roll with modifiers (e.g., +2, -1, etc.).
- Roll with advantage.
- Roll with Text to Speech enabled.
- Magic 8 ball functionality, answer to any questions using predetermined answers
- Get a random movie quote from Keanu Reeves in the chat
- If in a voice channel, play the movie quote in the voice channel
- Open a Minecraft server directly using one of the bot's commands

## Getting Started

### Prerequisites

Before you can add the Dice Roll Bot to your Discord server, you'll need the following:

- A Discord account.
- Administrative privileges on the Discord server where you want to add the bot.
- Node version 18.17.1 or newer

### Installation

1. **Invite the Bot to Your Server:**

    - Follow [these](https://discordpy.readthedocs.io/en/stable/discord.html) steps to create a bot account and to invite it on a server.
    - Make sure you remember the bot token when creating the bot so that you can use it later

2. **Set Up the Bot:**

    - Create an .env file to the root of the application with following information:
        ```
        DISCORD_TOKEN = [YOUR_DISCORD_TOKEN] #required
        BAT_FILE = [YOUR_BAT_FILE_PATH_TO_OPEN_MINECRAFT_SERVER] #optional
        MY_USER_ID = [YOUR_DISCORD_ID] #optional
        EMOJI_POS = [ID_OF_CHOSEN_EMOJI] #optional
        EMOJI_NEG = [ID_OF_CHOSEN_EMOJI] #optional
        ```
    - Open command prompt or terminal, navigate to the root of the application and enter the command:
        `tsc && node out/bot.js`

    Bot is correctly set up and running if you get the message "[YOUR_BOT_NAME] is online" in the command prompt. You should now see that the bot is online in the server that you invited it in.
    (**Please note** that the bot is only online when it is running in your computer. YOu need to restart it manually if you shut down your computer and open it up again)

## Usage

Once the bot is added to your server, configured and running, you can use it by either providing a slash command or custom command. Custom command for example:
`!roll 2d8 + 1`

Commands are divided into two different types: Slash commands and custom commands. Slash commands are basic commands that have certain functionality without the posibility for additional arguments. Custom commands consist of two parts: command prefix and arguments. The command prefix is a predefined trigger word or symbol, while the arguments are additional inputs provided by the user that modify the behavior of the command.

Here is a list of all commands available to the bot:
- Slash commands
  - /d4, /d6, /d8, /d10, /d12, /d20, /d100
    - Roll a single d4, d6, d8 etc. dice.
  - /help
    - Show an example usage of !roll commands
  - /minecraft
    - Starts a Minecraft server using a batch file. This requires that you know how to start a Minecraft server using a batch file, have BAT_FILE path defined in the .env file and have MY_USER_ID defined in the .env file so that no other user than you can start the batch file in your computer.
  - /whoa
    - Replies with a random movie quote from Keanu Reeves using [Keanu Reeves API](https://whoa.onrender.com/). If the user invoking this command is in a voice channel, the bot will additionally join the voice channel and play an audio clip of the movie quote.
- Custom commands
  - !roll
    - Using !roll-command, you can determine the multiplier, dice type and modifiers of the roll. For example "!roll 2d6 + 1" will roll two six-sided dice and add one to the roll
  - !rolladvantage
    - Using !rolladvantage-command, the bot will roll two of the provided dice regardless of the multiplier and pick greater of the two.
  - !rolltts
    - This command functions exactly the same as the !roll-command, but the answer will be spoken out loud using Discord's Text to Speech.
  - !8ballin
    - This command functions as a magic 8 ball. You can ask it a question and the bot will answer using predetermined answers found in the [answers.txt](answers.txt) file.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENCE.md)
