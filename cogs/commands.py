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

    # Need global Ratelimit maybe 2 mins between each
    @commands.command(name="search", guild_ids=[642556556680101903])
    async def search(self, ctx, arg=None):
        if arg is not None:
            if validators.url(arg) == True:
                if self.limit is False:
                    url = arg
                    self.limit = True
                    
                    # Display messages to user about bot
                    searchingEmbed = discord.Embed(title="Searching...", color=0xeb7100)
                    searchingEmbed.set_footer(text="This may take a while.")
                    searchingMessage = await ctx.send(embed=searchingEmbed)

                    # Displays the answer for Chapter Questions
                    answerRaw = cheinsteinpy.answer(url, self.cookie, self.userAgent)
                    if cheinsteinpy.parsers.checkLink(url) is True:
                        for count, step in enumerate(answerRaw):
                            count = count + 1
                            await ctx.send(f"**Step: {str(count)}**")
                            description = ""
                            for word in step.split():
                                if validators.url(word):
                                    if(len(description) > 0):
                                        await ctx.send(description)
                                    await ctx.send(word)
                                    description = ""
                                else:
                                    description = description + word + " "
                            if(len(description) > 0):
                                await ctx.send(description)
                    
                    # Displays the answer for Normal Questions
                    else:
                        for word in answerRaw:
                            if validators.url(word):
                                if(len(description) > 0):
                                    await ctx.send(description)
                                await ctx.send(word)
                                description = ""
                            else:
                                description = description + word + " "
                        if(len(description) > 0):
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