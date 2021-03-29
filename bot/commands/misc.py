import discord
from discord.ext import commands


class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='echo')
    async def command_echo(self, ctx, arg):
        await ctx.send(arg)
