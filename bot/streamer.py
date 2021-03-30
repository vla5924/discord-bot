import discord
import os
import youtube_dlc
from .song import Song
from collections import deque


class Streamer:
    def __init__(self, bot, client):
        self.bot = bot
        self.client = client
        self.queue = deque()
        self.current_song = None

    async def add_to_queue(self, query_string: str) -> Song:
        song = Song()
        # Check if query string is YT link
        if query_string.startswith('https://www.youtube.com/'):
            song.page_url = query_string
        # Or search with youtube_dlc otherwise
        else:
            options = {
                'format': 'bestaudio/best',
                'default_search': 'auto',
                'noplaylist': True
            }
            with youtube_dlc.YoutubeDL(options) as ydl:
                yt_entry = ydl.extract_info(query_string, download=False)
                video_id = yt_entry['entries'][0]['id']
                song.page_url = 'https://www.youtube.com/watch?v={}'.format(
                    video_id)
        downloader = youtube_dlc.YoutubeDL(
            {'format': 'bestaudio', 'title': True})
        yt_entry = downloader.extract_info(song.page_url, download=False)
        song.file_url = yt_entry.get('url')
        song.uploader = yt_entry.get('uploader')
        song.title = yt_entry.get('title')
        song.duration = yt_entry.get('duration')
        song.page_url = yt_entry.get('webpage_url')
        self.queue.append(song)
        if self.current_song is None:
            self.try_play_next_song()
        return song

    async def play_song(self, song: Song):
        ffmpeg = os.path.join(os.path.dirname(__file__), '..', 'ffmpeg')
        self.client.play(discord.FFmpegPCMAudio(song.file_url, executable=ffmpeg,
                         before_options='-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5'),
                         after=lambda error: self.try_play_next_song())

    def try_play_next_song(self):
        if len(self.queue) == 0:
            self.current_song = None
            return
        self.current_song = self.queue.pop()
        self.bot.loop.create_task(self.play_song(self.current_song))

    async def stop(self):
        if self.client is None or (not self.client.is_paused() and not self.client.is_playing()):
            return
        self.client.stop()
        self.current_song = None
        self.queue.clear()

    def clear_queue(self):
        self.queue.clear()

    def get_current_song(self) -> Song:
        return self.current_song
