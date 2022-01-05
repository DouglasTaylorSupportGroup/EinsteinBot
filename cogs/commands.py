import discord
from discord.ext import commands
import validators
import json
import cheinsteinpy 

with open("config.json", "r") as f:
    config = json.load(f)

with open("cookie.txt", 'r') as f:
    cookieTxt = f.read()

class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.limit = False
        self.cookie = cookieTxt
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

                    answerRaw = cheinsteinpy.answer(url, self.cookie, self.userAgent)
                    for word in answerRaw.split():
                        if validators.url(word):
                            ctx.send(word)
                        else:
                            description = description + word
                            await ctx.send(description)
                    
            elif validators.url(arg) != True:
                urlError = discord.Embed(title="Error", color=0xff4f4f, description="You need to provide a vaild URL.")
                await ctx.send(embed=urlError)
                return
            else:
                completeError = discord.Embed(title="Error", color=0xff4f4f, description="Something went wrong. Create an issue here for support: https://github.com/DouglasTaylorSupportGroup/EinsteinBot")
                await ctx.send(embed=completeError, delete_after=5.0)
                return
        else:
            argError = discord.Embed(title="Error", color=0xff4f4f, description="You need to provide a vaild URL.")
            await ctx.send(embed=argError)
            return
        
def setup(bot):
    bot.add_cog(Commands(bot))