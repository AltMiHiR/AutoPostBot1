from config import *

from pyrogram import filters

from MBot import app
from MBot.utils.database import *


@app.on_message(filters.private & filters.command("help") & filters.user(OWNER_ID))
async def group_chats(client, message):
    caption = f"""🥀 <u>**All Commands Menu:**</u> ✨

» `.sm` - reply to a message to
repeat message.

» `.st` [value] - to set repeat delay
timer [give value in second]
an example: `.st 10`

» `.ac` [chat_id] - add a chat id to
send message in that chat.
ex: `.ac -100123456789`

» `.dc` [chat_id] - remove a chat id
from database.
ex: `.dc -100123456789`

» `.gc` - get all active chat id's in
database.

» `.dly` [timer] - to set delay timer
for groups when sending messages.
ex: `.dly 5`

(set time value 0 to disable)"""
    await message.reply_text(caption)
