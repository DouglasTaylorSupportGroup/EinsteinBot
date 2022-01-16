from discord.ext import commands

def shared_cooldown(rate, per, type=commands.BucketType.default):
    cd = commands.Cooldown(rate, per)
    def decorator(func):
        if isinstance(func, commands.Command):
            func._buckets = commands.CooldownMapping.from_cooldown(rate, per, type)
        else:
            func.__commands_cooldown__ = commands.CooldownMapping(cd, type)
        return func
    return decorator

class ratelimit:
    searchCooldown = shared_cooldown(1, 10, commands.BucketType.default)