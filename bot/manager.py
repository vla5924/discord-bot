from .streamer import Streamer


class Manager:
    streamers = {}

    def __init__(self):
        raise NotImplementedError("Manager must be a singleton")

    @classmethod
    def register(cls, bot, guild, client):
        cls.streamers[guild] = Streamer(bot, client)

    @classmethod
    def unregister(cls, guild):
        del cls.streamers[guild]

    @classmethod
    def is_registered(cls, guild) -> bool:
        return guild in cls.streamers

    @classmethod
    def get(cls, guild) -> Streamer:
        return cls.streamers[guild] if cls.is_registered(guild) else None
