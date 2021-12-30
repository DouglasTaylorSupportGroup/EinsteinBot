import discord
from discord.ext import commands
import validators

class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.limit = False

    # need global ratelimit maybe 2 mins between each
    @commands.command(name="search", guild_ids=[642556556680101903])
    async def search(self, ctx, arg=None):
        if arg is not None:
            if validators.url(arg) == True:
                if self.limit is False:
                    self.limit = True
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