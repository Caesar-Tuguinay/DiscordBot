import os
import random

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("https://quizlet.com/"):
        author = message.author
        response = "valid"
        await message.channel.send(response)
    else:
        await message.channel.send("invalid")

client.run(TOKEN)