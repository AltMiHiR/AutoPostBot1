from config import API_ID, API_HASH, BOT_TOKEN

from pyromod import Client as MClient

from pyrogram import Client

from MBot.logging import LOGGER
from MBot.utils.data import BOT_COMMANDS

BOT_ID = BOT_TOKEN.split(":", 1)[0]


class MBot(MClient):
    def __init__(self):
        super().__init__("MBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN, plugins=dict(root="MBot/modules"))
    
    async def start(self):
        await super().start()
        me = await self.get_me()
        self.id = me.id
        self.username = me.username

        # Set Bot Commands
        is_set = await self.set_bot_commands(BOT_COMMANDS)
        if is_set:
            LOGGER.info("Bot Commands Set.")
        else:
            LOGGER.info("Failed to Set Bot Commands.")


class MUserbot(Client):
    def __init__(self, session: str):
        self.proxy_generator = self.get_proxy()
        proxy = next(self.proxy_generator)
        super().__init__("MUserbot", api_id=API_ID, api_hash=API_HASH, session_string=session, plugins=dict(root="MBot/plugins"), no_updates=False, proxy=proxy)

    def get_proxy(self):
        PROXIES = [
            {
                "hostname": "103.167.33.5",
                "scheme": "socks5",
                "port": 59101,
                "username": "9919harshit",
                "password": "UoqPXdyQpz",
                "slot": 4,
                "index": 7
            }
        ]
        while True:
            for proxy_doc in PROXIES.copy():
                yield proxy_doc

    async def start(self):
        await super().start()
        me = await self.get_me()
        self.id = me.id

    async def change_proxy(self):
        await self.stop()
        self.proxy = next(self.proxy_generator)
        await self.start()


app = MBot()
