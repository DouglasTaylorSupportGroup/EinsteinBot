import discord
from discord.ext import commands

from core.utils import send

class Link(discord.ui.View):
    def __init__(self, link, label):
        super().__init__()
        self.add_item(discord.ui.Button(label=label, url=link))

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
        embed.add_field(name="=source", value="Displays the bot's GitHub repository.", inline=False)
        embed.add_field(name="=search `url`", value="Searches for the answer within a Chegg link.", inline=False)
        await send(ctx, embed, True)

    @commands.command(name="source")
    async def source(self, ctx):
        label = "GitHub"
        link = "https://github.com/DouglasTaylorSupportGroup/EinsteinBot"
        embed = discord.Embed(title="Source Code", color=0x3083e3, description="EinsteinBot is open source and can be found on GitHub. Any issues or suggestions can be raised there.")
        embed.set_author(name="EinsteinBot", icon_url=self.bot.user.avatar.url)
        embed.set_footer(text="If you like the bot, consider leaving a star ⭐ on the repository, it helps a ton :D.")
        await send(ctx, embed, True, Link(link, label))

def setup(bot):
    bot.add_cog(Information(bot))