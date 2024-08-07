from config import API_ID, API_HASH, BOT_TOKEN

from pyromod import Client as MClient

from pyrogram import Client
from pyrogram.enums import ChatType

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
        proxy = {
            "hostname": "103.167.33.5",
            "scheme": "socks5",
            "port": 59101,
            "username": "9919harshit",
            "password": "UoqPXdyQpz",
            # "slot": 4,
            # "index": 7
        }
        super().__init__("MUserbot", api_id=API_ID, api_hash=API_HASH, session_string=session, plugins=dict(root="MBot/plugins"), no_updates=False, proxy=proxy)

    async def start(self):
        await super().start()
        me = await self.get_me()
        self.id = me.id

    async def fetch_chats(self):
        group_ids = []
        try:
            async for dialog in self.get_dialogs():
                if dialog.chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]:
                    group_ids.append(dialog.chat.id)
        except:
            return None
        return group_ids


app = MBot()
