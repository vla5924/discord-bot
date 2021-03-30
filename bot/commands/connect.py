import discord
from discord.ext import commands

from .. import utils, phrases
from ..manager import Manager


class Connect(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='connect', aliases=['c'])
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
        client = await voice.channel.connect(reconnect=True, timeout=None)
        Manager.register(self.bot, ctx.guild, client)
        await ctx.send("{}: {}".format(phrases.CONNECTED_TO_VOICE_CHANNEL, voice.channel.name))

    @commands.command(name='disconnect', aliases=['d'])
    async def command_disconnect(self, ctx):
        guild = ctx.guild
        if Manager.is_registered(guild):
            streamer = Manager.get(guild)
            await streamer.client.disconnect()
            Manager.unregister(guild)
            await ctx.send(phrases.DISCONNECTED)
        else:
            await ctx.send(phrases.ALREADY_DISCONNECTED)
