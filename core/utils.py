import discord
from sys import platform

async def send(ctx, message, isEmbed, view=None):
    if isEmbed:
        if isinstance(ctx, discord.ApplicationContext):
            if view is not None:
                await ctx.respond(embed=message, view=view)
            else:
                await ctx.respond(embed=message)
        else:
            if view is not None:
                await ctx.send(embed=message, view=view)
            else:
                await ctx.send(embed=message)
    else:
        if isinstance(ctx, discord.ApplicationContext):
            if view is not None:
                await ctx.respond(message, view=view)
            else:
                await ctx.respond(message)
        else:
            if view is not None:
                await ctx.send(message, view=view)
            else:
                await ctx.send(message)

async def sendDefer(ctx, message, isEmbed):
    if isEmbed:
        if isinstance(ctx, discord.ApplicationContext):
            await ctx.send_followup(embed=message)
        else:
            await ctx.send(embed=message)
    else:
        if isinstance(ctx, discord.ApplicationContext):
            await ctx.send_followup(message)
        else:
            await ctx.send(message)

async def callCommand(command, self, ctx, parameter=None):
    if platform.startswith("linux"):
        if parameter is None:
            await command(self, ctx)
        else:
            await command(ctx, parameter)
    else:
        if parameter is None:
            await command(ctx)
        else:
            await command(ctx, parameter)