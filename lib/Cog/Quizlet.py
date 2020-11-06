import os
from webbot import Browser
from bs4 import BeautifulSoup
from discord.ext import commands


class Quizlet(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.fcs = []

    @commands.command(description="To pull flashcards from link")
    async def link(self, ctx, message: str):
        if message.startswith("quizlet.com") or message.startswith("https://quizlet.com/"):
            try:
                await ctx.send('Trying to log into Quizlet. Give me some time UwU.')
                username = os.getenv('Q_USERNAME')
                password = os.getenv('Q_PASSWORD')
                username = str(username)
                password = str(password)
                link = message
                web = Browser()
                web.go_to(link)
                for x in (1, 10):
                    web.click('Log in', tag='button', loose_match=False)
                await ctx.send('Logging in')
                web.type(username, into='username')
                web.type(password, into='password')
                web.click('Log in', tag='button')
                await ctx.send('Extracting HTML')
                html = web.get_page_source()
                soup = BeautifulSoup(html, 'html.parser')
                results = soup.find_all('div', class_='SetPageTerms-term')
                await ctx.send('First 5 Flashcards:')
                x = 0
                self.fcs.clear()
                for result in results:
                    x = x + 1
                    result = str(result)
                    result_soup = BeautifulSoup(result, 'html.parser')
                    left_term = result_soup.find(class_="TermText notranslate lang-tl").get_text()
                    if "__" in left_term:
                        left_term = "\\" + left_term
                    right_term = result_soup.find(class_="TermText notranslate lang-en").get_text()
                    if "__" in right_term:
                        right_term = "\\" + right_term
                    self.fcs.append(left_term)
                    self.fcs.append(right_term)
                    if result is not None and x <= 5:
                        await ctx.send('Left Term: ' + left_term + '. Right Term: ' + right_term + '.')
                await ctx.send('If you wish to save this flashcard set, use command "!store title_of_set"')

            except (ValueError, Exception):
                await ctx.send('Invalid Quizlet Flashcard URL')
        else:
            await ctx.send('Invalid Quizlet Flashcard URL')

    @commands.command(description='For storing Flashcards')
    async def store(self, ctx, title: str):
        await ctx.send('Lol not ready yet XDDDDDDDDDDDDDDDD')


def setup(bot):
    bot.add_cog(Quizlet(bot))
