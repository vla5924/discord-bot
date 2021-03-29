import discord
from discord.ext import commands

from .. import utils, phrases
from ..manager import Manager


class Connect(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='connect')
    async def command_connect(self, ctx):
        if Manager.is_registered(ctx.guild):
            await ctx.send(phrases.ALREADY_CONNECTED)
            return
        voice = ctx.author.voice
        if voice is None:
            await ctx.send(phrases.MEMBER_NOT_IN_CHANNEL)
            return
        current_guild = utils.get_guild(self.bot, ctx.message)
        if current_guild is None:
            await ctx.send(phrases.NO_GUILD)
            return
        client = await voice.channel.connect()
        Manager.register_client(ctx.guild, client)
        await ctx.send("Connected to {}".format(voice.channel.name))

    @commands.command(name='disconnect')
    async def command_disconnect(self, ctx):
        guild = ctx.guild
        if Manager.is_registered(guild):
            client = Manager.get_client(guild)
            await client.disconnect()
            Manager.unregister_client(guild)
            await ctx.send("Disconnected")
        else:
            await ctx.send(phrases.ALREADY_DISCONNECTED)
