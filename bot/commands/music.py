import discord
from discord.ext import commands
from ..manager import Manager
from .. import phrases


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='play', aliases=['p'])
    async def command_play(self, ctx, *, query_string: str):
        if not Manager.is_registered(ctx.guild):
            await ctx.send(phrases.CONNECT_BEFORE_PLAYING)
            return
        streamer = Manager.get(ctx.guild)
        song = await streamer.add_to_queue(query_string)
        await ctx.send('{}: {} - {}'.format(phrases.ADDED_TO_QUEUE, song.uploader, song.title))

    @commands.command(name='stop', aliases=['s'])
    async def command_stop(self, ctx):
        if not Manager.is_registered(ctx.guild):
            await ctx.send(phrases.CONNECT_BEFORE_PLAYING)
            return
        streamer = Manager.get(ctx.guild)
        await streamer.stop()
    
    @commands.command(name='what', aliases=['w'])
    async def command_what(self, ctx):
        if not Manager.is_registered(ctx.guild):
            await ctx.send(phrases.NOTHING_IS_PLAYING)
            return
        streamer = Manager.get(ctx.guild)
        song = streamer.get_current_song()
        if song is None:
            await ctx.send(phrases.NOTHING_IS_PLAYING)
            return
        await ctx.send("{}: {} - {}".format(phrases.NOW_PLAYING, song.uploader, song.title))
