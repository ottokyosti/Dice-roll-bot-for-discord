import { CommandInteraction, Client, ApplicationCommandType, GuildMember, VoiceBasedChannel } from "discord.js";
import { Command } from "./Command";
import axios from "axios";
import { joinVoiceChannel, createAudioPlayer, createAudioResource, AudioPlayerStatus } from "@discordjs/voice";
import _sodium from "libsodium-wrappers";
import child, { ChildProcess } from "child_process";
require("dotenv").config();

const d4: Command = {
    name: "d4",
    description: "Roll a d4 dice",
    type: ApplicationCommandType.ChatInput,
    run: async (client: Client, interaction: CommandInteraction) => {
        const result = getDiceRoll(1, 4).toString();

        await interaction.followUp({
            ephemeral: false,
            content: `You rolled a ${result} on a d4 dice!`
        });
    }
}

const d6: Command = {
    name: "d6",
    description: "Roll a d6 dice",
    type: ApplicationCommandType.ChatInput,
    run: async (client: Client, interaction: CommandInteraction) => {
        const result = getDiceRoll(1, 6).toString();

        await interaction.followUp({
            ephemeral: false,
            content: `You rolled a ${result} on a d6 dice!`
        });
    }
}

const d8: Command = {
    name: "d8",
    description: "Roll a d8 dice",
    type: ApplicationCommandType.ChatInput,
    run: async (client: Client, interaction: CommandInteraction) => {
        const result = getDiceRoll(1, 8).toString();

        await interaction.followUp({
            ephemeral: false,
            content: `You rolled a ${result} on a d8 dice!`
        });
    }
}

const d10: Command = {
    name: "d10",
    description: "Roll a d10 dice",
    type: ApplicationCommandType.ChatInput,
    run: async (client: Client, interaction: CommandInteraction) => {
        const result = getDiceRoll(1, 10).toString();

        await interaction.followUp({
            ephemeral: false,
            content: `You rolled a ${result} on a d10 dice!`
        });
    }
}

const d12: Command = {
    name: "d12",
    description: "Roll a d12 dice",
    type: ApplicationCommandType.ChatInput,
    run: async (client: Client, interaction: CommandInteraction) => {
        const result = getDiceRoll(1, 12).toString();

        await interaction.followUp({
            ephemeral: false,
            content: `You rolled a ${result} on a d12 dice!`
        });
    }
}

const d20: Command = {
    name: "d20",
    description: "Roll a d20 dice",
    type: ApplicationCommandType.ChatInput,
    run: async (client: Client, interaction: CommandInteraction) => {
        const result = getDiceRoll(1, 20).toString();

        await interaction.followUp({
            ephemeral: false,
            content: `You rolled a ${result} on a d20 dice!`
        });
    }
}

const d100: Command = {
    name: "d100",
    description: "Roll a d100 dice",
    type: ApplicationCommandType.ChatInput,
    run: async (client: Client, interaction: CommandInteraction) => {
        const result = getDiceRoll(1, 100).toString();

        await interaction.followUp({
            ephemeral: false,
            content: `You rolled a ${result} on a d100 dice!`
        });
    }
}

const whoa: Command = {
    name: "whoa",
    description: "Get a random movie line from the famous actor John",
    type: ApplicationCommandType.ChatInput,
    run: async (client: Client, interaction: CommandInteraction) => {
        const response = await axios.get("https://whoa.onrender.com/whoas/random?group_whoa_assets=false");
        const data = response.data[0];
        const reply: string = `**"${data.full_line}"** - **Keanu Reeves** as **${data.character}** in **${data.movie}** at **${data.timestamp}**`;

        const member: GuildMember | null = interaction.member as GuildMember;
        const voiceChannel: VoiceBasedChannel | null = member?.voice.channel;

        if (voiceChannel != null) {
            await _sodium.ready;
            const connection = joinVoiceChannel({
                channelId: voiceChannel.id,
                guildId: interaction.guildId!,
                adapterCreator: interaction.guild!.voiceAdapterCreator!,
            });
          
            const audioPlayer = createAudioPlayer();
            const stream = data.audio;
            const resource = createAudioResource(stream);
          
            audioPlayer.play(resource);
            connection.subscribe(audioPlayer);
          
            audioPlayer.on(AudioPlayerStatus.Idle, () => {
                connection.destroy();

                interaction.followUp({
                    ephemeral: false,
                    content: reply
                });
            });
        } else {
            await interaction.followUp({
                ephemeral: false,
                content: reply
            });
        }
    }
}

const minecraft: Command = {
    name: "minecraft",
    description: "Starts a minecraft server on users local computer",
    type: ApplicationCommandType.ChatInput,
    run: async (client: Client, interaction: CommandInteraction) => {
        const currentUser: string = interaction.user.id;
        if (process.env.MY_USER_ID == undefined) {
            await interaction.followUp({
                ephemeral: true,
                content: "MY_USER_ID is not defined"
            });
            return;
        }

        if (currentUser != process.env.MY_USER_ID) {
            await interaction.followUp({
                ephemeral: true,
                content: "This command is restricted to the owner of the bot"
            });
            return;
        }

        if (process.env.BAT_FILE_PATH != null) {
            child.exec(`start cmd.exe /c "${process.env.BAT_FILE_PATH}"`, (error, stdout, stderr) => {});

            await interaction.followUp({
                ephemeral: false,
                content: "Minecraft server is starting..."
            });
        } else {
            await interaction.followUp({
                ephemeral: true,
                content: "BAT_FILE environment variable is not defined"
            });
        }
    }
}

const help: Command = {
    name: "help",
    description: "Show example usage of !roll commands",
    type: ApplicationCommandType.ChatInput,
    run: async (client: Client, interaction: CommandInteraction) => {
        await interaction.followUp({
            ephemeral: true,
            content: "Template usage of !roll command: !roll <multiplier>d<dice> <+/-> <modifier> <+/-> <modifier> ... (for example: !roll 3d4 + 2 - 1)"
        });
    }
}

const getDiceRoll = (min: number, max: number) => {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

export default [d4, d6, d8, d10, d12, d20, d100, whoa, minecraft, help];