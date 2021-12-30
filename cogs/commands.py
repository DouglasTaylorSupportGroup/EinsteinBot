import discord
from discord.ext import commands
import validators
import json
from core import cookie
from core.scraper import request, parse

with open("config.json", "r") as f:
    config = json.load(f)

class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.limit = False
        self.cookieStr = cookie.parseCookie("cookie.txt")
        self.userAgent = config["userAgent"]

    # need global ratelimit maybe 2 mins between each
    @commands.command(name="search", guild_ids=[642556556680101903])
    async def search(self, ctx, arg=None):
        if arg is not None:
            if validators.url(arg) == True:
                if self.limit is False:
                    url = arg
                    self.limit = True
                    searchingEmbed = discord.Embed(title="Searching...", color=0xeb7100)
                    searchingEmbed.set_footer(text="This may take a while.")
                    searchingMessage = await ctx.send(embed=searchingEmbed)

                    htmlData = request.requestWebsite(url, self.cookieStr, self.userAgent)
                    isChapter = parse.checkLink(url)
                    dataRaw = parse.parsePage(htmlData, isChapter)
                    if isChapter:
                        data = dataRaw
                    else:
                        data = dataRaw[1]
                    answerRaw = parse.getAnswer(data, isChapter)
                    
            elif validators.url(arg) != True:
                urlError = discord.Embed(title="Error", color=0xff4f4f, description="You need to provide a vaild URL.")
                await ctx.respond(embed=urlError)
                return
            else:
                completeError = discord.Embed(title="Error", color=0xff4f4f, description="Something went wrong. Create an issue here for support: https://github.com/The-Brandon-Tran/EinsteinBot")
                await ctx.send(embed=completeError, delete_after=5.0)
                return
        else:
            argError = discord.Embed(title="Error", color=0xff4f4f, description="You need to provide a vaild URL.")
            await ctx.respond(embed=argError)
            return
        
def setup(bot):
    bot.add_cog(Commands(bot))