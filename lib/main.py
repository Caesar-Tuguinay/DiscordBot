import os
import random
import requests

import discord
from webbot import Browser
from dotenv import load_dotenv
from bs4 import BeautifulSoup

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')

@client.event
async def on_message(message):
    if message.content == '!options':
        channel = message.channel
        author = message.author
        await channel.send('Choose:')
        await channel.send('Least Squares')
        await channel.send('or')
        await channel.send('NLP')

        def check_math(m):
            return m.content == 'Least Squares' and m.channel == channel and m.author == author

        def check_nlp(m):
            return m.content == 'NLP' and m.channel == channel and m.author == author

        def check_all(m):
            return check_math(m) or check_nlp(m)

        msg = await client.wait_for('message', check=check_all)
        await channel.send('Nice choice {.author}! But this is not ready yet.'.format(msg))

client.run(TOKEN)