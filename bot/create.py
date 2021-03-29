import discord
from discord.ext import commands

from .music import Music
from .connect import Connect
from . import phrases

def create(prefix):
    bot = commands.Bot(command_prefix=prefix)
    bot.add_cog(Music(bot))
    bot.add_cog(Connect(bot))
    async def on_command_error(ctx, exception):
        await ctx.send(phrases.COMMAND_NOT_FOUND)
    bot.on_command_error = on_command_error
    return bot
