import * as Discord from "discord.js";
import Commands from "./commands";
import interactionCreate from "./listeners/interactionCreate";
import roll from "./diceRoll";
import { readFileSync } from "fs";
require("dotenv").config();

console.log("Bot is starting...");

const answers: string[] = readFileSync("./answers.txt", "utf-8").split("\n");

const token = process.env.DISCORD_TOKEN;

const client = new Discord.Client({
    intents: ["Guilds", "GuildMessages", "MessageContent", "GuildVoiceStates"]
});

const getRandomAnswer = (): string => {
    const length: number = answers.length;
    return answers[Math.floor(Math.random() * length)];
}

client.on("ready", async () => {
    if (!client.user || !client.application) {
        return;
    }

    await client.application.commands.set(Commands);

    console.log(`${client.user.username} is online`);
});

client.on("messageCreate", msg => {
    if (msg.author.bot) return;

    if (msg.content.includes("!rolladvantage")) {
        const options = {
            content: roll(msg.content, true),
            tts: false
        }
        try {
            msg.channel.send(options);
        } catch (error) {
            msg.channel.send("I can't decode your roll");
        }
        return;
    } else if (msg.content.includes("!rolltts")) {
        const options = {
            content: roll(msg.content, false),
            tts: true
        }
        try {
            msg.channel.send(options);
        } catch (error) {
            msg.channel.send("I can't decode your roll!");
        }
        return;
    } else if (msg.content.includes("!roll")) {
        try {
            msg.reply(roll(msg.content, false));
        } catch (error) {
            msg.reply("I can't decode your roll!");
        }
        return;
    }
    
    if (msg.content.includes("!8ballin")) {
        const options = {
            content: getRandomAnswer(),
            tts: true
        }
        try {
            msg.channel.send(options);
        } catch (error) {
            msg.channel.send("Voi vittu, jotain meni rikki!");
        }
        return;
    }
});

interactionCreate(client);

client.login(token);