import asyncio

from pyrogram import idle

from MBot import app
from MBot.logging import LOGGER


async def init():
    LOGGER.info("Starting Bot ...")
    await app.start()
    LOGGER.info("Bot Started Successfully")
    await idle()
    await app.stop()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init())
    LOGGER.info("Bot Stopped !")
