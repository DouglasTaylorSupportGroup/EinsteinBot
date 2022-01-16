import re
import discord
from discord.ext import commands
import validators
import json
import cheinsteinpy

from core.utils import sendDefer, send
from core.ratelimit import ratelimit

with open("config.json", "r") as f:
    config = json.load(f)

with open("cookie.txt", 'r') as f:
    cookieTxt = f.read()

class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cookie = cookieTxt
        self.userAgent = config["userAgent"]

    # Need global Ratelimit maybe 2 mins between each
    @commands.command(name="search")
    #@commands.cooldown(1, 15, commands.BucketType.default)
    @ratelimit.searchCooldown
    async def search(self, ctx, url=None):
        if url is not None:
            if validators.url(url) == True:
                if "chegg.com/homework-help" in url:
                    answerRaw = cheinsteinpy.answer(url, self.cookie, self.userAgent)
                    # Displays the answer for Chapter Questions
                    if answerRaw is None:
                        errorEmbed = discord.Embed(title="Error", description="Something went wrong or there was no solution.", color=0xff4f4f)
                        await sendDefer(ctx, errorEmbed, True)
                    else:
                        if cheinsteinpy.checkLink(url) is True:
                            for count, step in enumerate(answerRaw):
                                count = count + 1
                                stepEmbed = discord.Embed(title=f"Step {str(count)}", color=0xeb7100)
                                await sendDefer(ctx, stepEmbed, True)
                                description = ""
                                for word in step.split():
                                    if validators.url(word):
                                        if(len(description) > 0):
                                            await sendDefer(ctx, description, False)
                                        await sendDefer(ctx, word, False)
                                        description = ""
                                    else:
                                        description = description + word + " "
                                if(len(description) > 0):
                                    await sendDefer(ctx, description, False)
                        
                        # Displays the answer for Normal Questions
                        else:
                            description = ""
                            regex = re.search("(?P<url>https?://[^\s]+)", answerRaw)
                            if regex is not None:
                                for word in answerRaw.split():
                                    if validators.url(word):
                                        if(len(description) > 0):
                                            await sendDefer(ctx, description, False)
                                        await sendDefer(ctx, word, False)
                                        description = ""
                                    else:
                                        description = description + word + " "
                                if(len(description) > 0):
                                    await sendDefer(ctx, description, False)
                            else:
                                if len(answerRaw) >= 6000:
                                    charCount = 0
                                    description = ""
                                    for word in answerRaw.split():
                                        charCount += len(word)
                                        if charCount >= 3000:
                                            embed = discord.Embed(title="Answer", description=description, color=0xeb7100)
                                            await sendDefer(ctx, embed, True)
                                            description = ""
                                            charCount = 0
                                        description = description + word + " "
                                else:
                                    embed = discord.Embed(title="Answer", description=answerRaw, color=0xeb7100)
                                    await sendDefer(ctx, embed, True)
                else:
                    urlError = discord.Embed(title="Error", color=0xff4f4f, description="You need to provide a vaild URL.")
                    await sendDefer(ctx, urlError, True)
                    return
            elif validators.url(url) != True:
                urlError = discord.Embed(title="Error", color=0xff4f4f, description="You need to provide a vaild URL.")
                await sendDefer(ctx, urlError, True)
                return
            else:
                completeError = discord.Embed(title="Error", color=0xff4f4f, description="Something went wrong. Create an issue here for support: https://github.com/DouglasTaylorSupportGroup/EinsteinBot")
                completeError.set_footer(text="ERROR001")
                await sendDefer(ctx, completeError, True)
                return
        else:
            argError = discord.Embed(title="Error", color=0xff4f4f, description="You need to provide a vaild URL.")
            await sendDefer(ctx, argError, True)
            return
    
    @search.error
    async def searchError(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(title="Global Rate-Limit", description=f"Please wait {round(error.retry_after)} seconds and try again.", color=0xeb7100)
            embed.set_footer(text="Avoids bot detection on Chegg.")
            await send(ctx, embed, True)
        else:
            completeError = discord.Embed(title="Error", color=0xff4f4f, description="Something went wrong. Create an issue here for support: https://github.com/DouglasTaylorSupportGroup/EinsteinBot")
            completeError.set_footer(text="ERROR002")
            await send(ctx, completeError, True)
            raise error
        
def setup(bot):
    bot.add_cog(Commands(bot))