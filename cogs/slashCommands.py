import discord
from discord.ext import commands
from cogs import info

class SlashCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="ping", guild_ids=[642556556680101903])
    async def ping_slash(self, ctx):
        await info.Information.ping(ctx)

    @commands.slash_command(name="help", guild_ids=[642556556680101903])
    async def help_slash(self, ctx):
        await info.Information.help(ctx)

def setup(bot):
    bot.add_cog(SlashCommands(bot))