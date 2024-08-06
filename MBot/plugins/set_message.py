from pyrogram import filters
from pyrogram.types import Message

from MBot import MUserbot
from MBot.utils.database import set_post


@MUserbot.on_message(filters.me & filters.command(["sm", "setmessage"]))
async def set_message_ids(client: MUserbot, message: Message):
    r_message = message.reply_to_message
    if r_message:
        if message.chat.id != client.id:
            r_message = await r_message.copy("me")
        set = await set_post(r_message.id)
    else:
        try:
            value = message.text.split(" ", 2)[1]
        except:
            await message.reply_text("Please Reply To a Message")
            return
        if value == "0":
            set = await set_post(0)
            if set:
                await message.reply_text("Successfully Reset")
                return
        else:
            await message.reply_text("Please Reply To a Message")
            return
