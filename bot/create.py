import discord
from discord.ext.commands import Bot

from .commands import Connect, Misc, Music
from . import phrases


def create(prefix):
    bot = Bot(command_prefix=prefix)

    bot.add_cog(Connect(bot))
    bot.add_cog(Misc(bot))
    bot.add_cog(Music(bot))

    async def on_command_error(ctx, exception):
        await ctx.send(phrases.COMMAND_NOT_FOUND)
    bot.on_command_error = on_command_error
    return bot
