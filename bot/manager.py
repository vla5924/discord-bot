class Manager:
    clients = {}

    def __init__(self):
        raise NotImplementedError("Manager must be a singleton")

    @classmethod
    def register_client(cls, guild, client):
        cls.clients[guild] = client

    @classmethod
    def unregister_client(cls, guild):
        del cls.clients[guild]

    @classmethod
    def is_registered(cls, guild):
        return guild in cls.clients

    @classmethod
    def get_client(cls, guild):
        return cls.clients[guild] if cls.is_registered(guild) else None
