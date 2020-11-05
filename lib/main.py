import os
import re
import random
import requests
import time
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
    if message.content.startswith("https://quizlet.com/"):
        link = message.content
        channel = message.channel
        web = Browser()
        web.go_to(link)
        await channel.send('Finding Login Info for Quizlet. Give me some time.')
        for x in (1,10):
            web.click('Log in', tag='button', loose_match=False)
        await channel.send('Logging in')
        web.type('', into = 'username')
        web.type('', into = 'password')
        web.click('Log in', tag='button')
        await channel.send('Extracting HTML')
        html = web.get_page_source()
        soup = BeautifulSoup(html, 'html.parser')
        results = soup.find_all('div', class_='SetPageTerms-term')
        for result in results:
            if result is not None:
                result = str(result)
                result = result.replace('"', '')
                result = result.replace('<', 'AAA')
                result = result.replace('>', 'BBB')
                result = result.replace('/', 'CCC')
                await channel.send(result)
                left_term = re.search("^tlBBB.*</span>$", result)
                right_term = re.search("^enBBB.*<$", result)
                await channel.send('Tagalog Term: ' + left_term + '. English Term: ' + right_term + '.')

client.run(TOKEN)