import discord
from discord.ext import commands
from cogs import info, main
from core.utils import send, callCommand
from core.ratelimit import ratelimit

class SlashCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="ping")
    async def ping_slash(self, ctx):
        await callCommand(info.Information.ping, self, ctx)

    @commands.slash_command(name="help")
    async def help_slash(self, ctx):
        await callCommand(info.Information.help, self, ctx)

    @commands.slash_command(name="source")
    async def source_slash(self, ctx):
        await callCommand(info.Information.source, self, ctx)

    @commands.slash_command(name="botinfo")
    async def botinfo_slash(self, ctx):
        await callCommand(info.Information.botinfo, self, ctx)

    @commands.slash_command(name="search")
    @ratelimit.searchCooldown
    async def search_slash(self, ctx, **url):
        await ctx.defer()
        urlReal = url["url"]
        await callCommand(main.Commands.search, self, ctx, urlReal)

    @search_slash.error
    async def search_slash_error(self, ctx, error):
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
    bot.add_cog(SlashCommands(bot))