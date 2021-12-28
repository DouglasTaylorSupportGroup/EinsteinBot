import discord
from discord.commands import slash_command
from discord.ext import commands

class Information(commands.Cog):
    
    # Constructor
    def __init__(self, bot):
        self.bot = bot
    
    # Checks the ping of the bot
    @slash_command(name="ping", guild_ids=[642556556680101903])
    async def ping(self, ctx):
        await ctx.respond(f"🏓 Pong! My ping is {round(self.bot.latency * 1000)}ms")

def setup(bot):
    bot.add_cog(Information(bot))