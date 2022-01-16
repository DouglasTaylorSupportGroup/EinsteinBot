import discord
from discord.ext import commands

from core.utils import send

class Information(commands.Cog):
    
    # Constructor
    def __init__(self, bot):
        self.bot = bot
    
    # Checks the ping of the bot
    @commands.command(name="ping")
    async def ping(self, ctx):
        ping = f"🏓 Pong! My ping is {round(self.bot.latency * 1000)}ms"
        await send(ctx, ping, False)

    @commands.command(name="help")
    async def help(self, ctx):
        embed = discord.Embed(title="Help", color=0x3083e3)
        embed.set_author(name="EinsteinBot", icon_url=self.bot.user.avatar.url)
        embed.add_field(name="=help", value="Display this message.", inline=False)
        embed.add_field(name="=ping", value="Displays the ping.", inline=False)
        embed.add_field(name="=search `url`", value="Searches for the answer within a Chegg link.", inline=False)
        await send(ctx, embed, True)

def setup(bot):
    bot.add_cog(Information(bot))