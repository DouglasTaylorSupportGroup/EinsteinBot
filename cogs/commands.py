import re
import discord
from discord.ext import commands
import validators
import json
import cheinsteinpy
import asyncio

with open("config.json", "r") as f:
    config = json.load(f)

with open("cookie.txt", 'r') as f:
    cookieTxt = f.read()

class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.limit = False
        self.commandRunning = False
        self.cookie = cookieTxt
        self.userAgent = config["userAgent"]

    # Need global Ratelimit maybe 2 mins between each
    @commands.command(name="search")
    @commands.cooldown(1, 20)
    async def search(self, ctx, arg=None):
        if arg is not None:
            if validators.url(arg) == True:
                if self.commandRunning is False:
                    self.commandRunning = True
                    url = arg

                    # Display messages to user about bot
                    searchingEmbed = discord.Embed(title="Searching...", color=0xeb7100)
                    searchingEmbed.set_footer(text="This may take up to 10 seconds.")
                    searchingMessage = await ctx.send(embed=searchingEmbed)

                    # Displays the answer for Chapter Questions
                    answerRaw = cheinsteinpy.answer(url, self.cookie, self.userAgent)
                    if answerRaw is None:
                        await searchingMessage.delete()
                        errorEmbed = discord.Embed(title="Error", description="Something went wrong or there was no solution.", color=0xff4f4f)
                        await ctx.send(embed=errorEmbed)
                    else:
                        if cheinsteinpy.checkLink(url) is True:
                            await searchingMessage.delete()
                            for count, step in enumerate(answerRaw):
                                count = count + 1
                                stepEmbed = discord.Embed(title=f"Step {str(count)}", color=0xeb7100)
                                await ctx.send(embed=stepEmbed)
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
                            await searchingMessage.delete()
                            description = ""
                            regex = re.search("(?P<url>https?://[^\s]+)", answerRaw)
                            if regex is not None:
                                for word in answerRaw.split():
                                    if validators.url(word):
                                        if(len(description) > 0):
                                            await ctx.send(description)
                                        await ctx.send(word)
                                        description = ""
                                    else:
                                        description = description + word + " "
                                if(len(description) > 0):
                                    await ctx.send(description)
                            else:
                                if len(answerRaw) >= 6000:
                                    charCount = 0
                                    description = ""
                                    for word in answerRaw.split():
                                        charCount += len(word)
                                        if charCount >= 3000:
                                            embed = discord.Embed(title="Answer", description=description, color=0xeb7100)
                                            await ctx.send(embed=embed)
                                            description = ""
                                            charCount = 0
                                        description = description + word + " "
                                else:
                                    embed = discord.Embed(title="Answer", description=answerRaw, color=0xeb7100)
                                    await ctx.send(embed=embed)
                            
                        self.commandRunning = False

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
    
    @search.error
    async def searchError(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(title="Global Rate-Limit", description=f"Please wait {round(error.retry_after)} seconds and try again.", color=0xeb7100)
            embed.set_footer(text="Avoids bot detection on Chegg.")
            await ctx.send(embed=embed)
        else:
            print(error)
        
def setup(bot):
    bot.add_cog(Commands(bot))