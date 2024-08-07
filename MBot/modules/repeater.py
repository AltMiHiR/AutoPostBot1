import asyncio

from time import time

from config import OWNER_ID

from pyrogram import filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait, UserDeactivatedBan, SlowmodeWait

from MBot import BOT_ID, app
from MBot.logging import LOGGER
from MBot.utils.database import *
from MBot.utils.userbot import get_userbot


POSTING_TASKS = {}


async def text_repeater():
    count = 0
    while True:
        userbot = await get_userbot()
        if not userbot:
            try:
                await app.send_message(OWNER_ID, "⛔ **ᴜsᴇʀʙᴏᴛ ᴀᴄᴄᴏᴜɴᴛ ɴᴏᴛ ᴀᴅᴅᴇᴅ.**\n\nᴘʟᴇᴀsᴇ ᴀᴅᴅ ɪᴛ ᴜsɪɴɢ /auth ᴄᴏᴍᴍᴀɴᴅ.\nᴛʀʏɪɴɢ ᴀɢᴀɪɴ ᴀғᴛᴇʀ 5 ᴍɪɴᴜᴛᴇs...")
            except:
                LOGGER.warning("Userbot Account Not Added. Add it using /auth command. ReTrying after 5 minutes...")
            await asyncio.sleep(300)
            continue

        chats = await get_served_chats()
        post_msg_id = await get_post()
        speed = await get_repeat_time()
        group_delay = await get_delay_time()

        if len(chats) == 0:
            await asyncio.sleep(speed)
        elif post_msg_id == 0:
            await asyncio.sleep(speed)
        else:
            t1 = time()
            for chat_id in chats:
                try:
                    await userbot.copy_message(chat_id, "me", post_msg_id)
                except FloodWait as e:
                    await asyncio.sleep(e.value + 2)
                    try:
                        await userbot.copy_message(chat_id, "me", post_msg_id)
                    except:
                        pass
                except SlowmodeWait:
                    continue
                except UserDeactivatedBan:
                    try:
                        await app.send_message(OWNER_ID, "Account is Banned.")
                    except:
                        LOGGER.warning("Account is Banned.")
                    return
                except Exception as e:
                    continue
                if group_delay > 0:
                    await asyncio.sleep(group_delay)
            t2 = time()
            sleep_times = speed - (t2 - t1)
            if sleep_times > 0:
                await asyncio.sleep(sleep_times)

        # count += 1
        # if count % 90 == 0:
        #     await userbot.change_proxy()
        #     try:
        #         await app.send_message(OWNER_ID, f"PROXY CHANGED: {userbot.proxy['hostname']}")
        #     except:
        #         LOGGER.info(f"PROXY CHANGED: {userbot.proxy['hostname']}")


@app.on_message(filters.private & filters.command('posting') & filters.user(OWNER_ID))
async def _posting(_, message: Message):
    global POSTING_TASKS
    posting_status = await get_posting_mode()
    try:
        mode = message.text.split(" ", 2)[1]
    except:
        await message.reply_text(f"⚠️ **Usage:** /posting [enable|disable]\n\nPosting Status = {'✅ Enabled' if posting_status else '⛔ Disabled'}")
        return

    if mode.lower() == "enable":
        if posting_status:
            await message.reply_text("✅ **ᴀʟʀᴇᴀᴅʏ ᴘᴏsᴛɪɴɢ...**")
            return
        if BOT_ID in POSTING_TASKS and POSTING_TASKS[BOT_ID]:
            task = POSTING_TASKS[BOT_ID]
            try:
                task.cancel()
            except:
                pass
        task = asyncio.create_task(text_repeater())
        POSTING_TASKS[BOT_ID] = task
        await set_posting_mode(True)
        await message.reply_text("✅ **ᴘᴏsᴛɪɴɢ sᴛᴀʀᴛᴇᴅ.**")
    else:
        if not posting_status:
            await message.reply_text("⛔ **ᴘᴏsᴛɪɴɢ ᴀʟʀᴇᴀᴅʏ sᴛᴏᴘᴘᴇᴅ.**")
            return
        if BOT_ID in POSTING_TASKS:
            task = POSTING_TASKS[BOT_ID]
            try:
                task.cancel()
            except:
                pass
            del POSTING_TASKS[BOT_ID]
        await set_posting_mode(False)
        await message.reply_text("✅ **ᴘᴏsᴛɪɴɢ sᴛᴏᴘᴘᴇᴅ.**")


async def start_posting():
    global POSTING_TASKS
    posting_status = await get_posting_mode()
    if posting_status:
        task = asyncio.create_task(text_repeater())
        POSTING_TASKS[BOT_ID] = task

asyncio.create_task(start_posting())
