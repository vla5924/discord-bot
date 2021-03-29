import discord
from discord.ext import commands

import config
import bot

my_bot = bot.create(config.BOT_PREFIX)
# my_bot = commands.Bot(command_prefix=config.BOT_PREFIX)


@my_bot.command(pass_context=True)
async def echo(ctx, arg):
    await ctx.send(arg)

my_bot.run(config.BOT_TOKEN)
