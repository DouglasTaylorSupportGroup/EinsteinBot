import discord
from discord.ext import commands
from cogs import info, main
from core.utils import send
from core.ratelimit import ratelimit

class SlashCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="ping", guild_ids=[642556556680101903])
    async def ping_slash(self, ctx):
        await info.Information.ping(self, ctx)

    @commands.slash_command(name="help", guild_ids=[642556556680101903])
    async def help_slash(self, ctx):
        await info.Information.help(self, ctx)

    @commands.slash_command(name="search", guild_ids=[642556556680101903])
    @ratelimit.searchCooldown
    async def search_slash(self, ctx, **url):
        await ctx.defer()
        url = url["url"]
        await main.Commands.search(self, ctx, url)

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