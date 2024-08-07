import os

from config import OWNER_ID

from pyrogram import filters
from pyrogram.types import Message

from MBot import app
from MBot.logging import LOG_FILE_NAME
from MBot.utils.userbot import get_userbot
from MBot.utils.database import set_repeat_time, set_delay_time, add_served_chat, del_served_chat, get_served_chats, get_repeat_time


@app.on_message(filters.private & filters.command(["sm", "setmessage"]) & filters.user(OWNER_ID))
async def _set_message(client, message: Message):
    await message.reply_text("⛔ **ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ғʀᴏᴍ ᴘᴏsᴛɪɴɢ ᴀᴄᴄᴏᴜɴᴛ.**")


@app.on_message(filters.private & filters.command("ids") & filters.user(OWNER_ID))
async def _fetch_ids(client, message: Message):
    mx = await message.reply_text("🔄️ **ғᴇᴛᴄʜɪɴɢ ᴄʜᴀᴛs...**")
    userbot = await get_userbot()
    group_data = await userbot.fetch_chats()

    if group_data == None:
        await message.reply_text("⛔ **ғᴀɪʟᴇᴅ ᴛᴏ ғᴇᴛᴄʜ ɢʀᴏᴜᴘs.**")
        return
    
    if len(group_data) == 0:
        await message.reply_text("⛔ **ɴᴏ ɢʀᴏᴜᴘ ᴄʜᴀᴛs ғᴏᴜɴᴅ.**")
        return
    
    text = "✅ Group Chats:"
    for ind, (group_id, group_name) in enumerate(group_data.items()):
        text += f"\n\n[{ind + 1}] {group_name} | {group_id}"

    file_name = f"Chats{userbot.id}.txt"
    with open(file_name, 'w') as gc_file:
        gc_file.write(text)

    try:
        await mx.delete()
    except:
        pass
    await message.reply_document(file_name, caption=f"✅ **ɢʀᴏᴜᴘ ᴄʜᴀᴛs ғᴇᴛᴄʜᴇᴅ.**\n\nAccount = {userbot.phone_number}", file_name="Groups.txt")
    try:
        os.remove(file_name)
    except:
        pass


@app.on_message(filters.private & filters.command(["st", "settime"]) & filters.user(OWNER_ID))
async def set_message_time(client, message: Message):
    try:
        timer_value = int(message.text.split(None, 1)[1])
    except:
        await message.reply_text(f"give me some time value in seconds.\n\nEx: `.st 10`")
        return
    if int(timer_value) == 0:
        await message.reply_text(f"time value need to set minium 1 sec !")
        return
    set = await set_repeat_time(timer_value)
    if set:
        await message.reply_text(f"Successfully Set time {timer_value} Seconds.")
        return
    await message.reply_text("Already Running with Same Time Value!")


@app.on_message(filters.private & filters.command(["dly", "delay"]) & filters.user(OWNER_ID))
async def set_group_time(client, message: Message):
    try:
        timer_value = int(message.text.split(None, 1)[1])
    except:
        await message.reply_text(f"give me some time value in seconds.\n\nEx: `.dly 2`")
        return
    set = await set_delay_time(timer_value)
    if set:
        if int(timer_value) == 0:
            await message.reply_text(f"group delay now disabled !")
            return
        await message.reply_text(f"Successfully Set time {timer_value} Seconds.")
        return
    await message.reply_text("Already Running with Same Time Value!")


@app.on_message(filters.private & filters.command(["ac", "addchat"]) & filters.user(OWNER_ID))
async def set_chats_ids(client, message: Message):
    try:
        chat_id = int(message.text.split(None, 1)[1])
    except:
        await message.reply_text("give me chat id")
        return
    if chat_id > 0:
        await message.reply_text("please give me correct chat id")
        return
    is_chat = await add_served_chat(chat_id)
    if is_chat:
        await message.reply_text("successfully added in my database")
        return
    await message.reply_text("already added in my database")
    

@app.on_message(filters.private & filters.command(["dc", "delchat"]) & filters.user(OWNER_ID))
async def del_chats_ids(client, message: Message):
    try:
        chat_id = int(message.text.split(None, 1)[1])
    except:
        await message.reply_text("give me chat id")
        return
    if chat_id > 0:
        await message.reply_text("please give me correct chat id")
        return
    is_chat = await del_served_chat(chat_id)
    if is_chat:
        await message.reply_text("successfully removed from my database")
        return
    await message.reply_text("chat id not active in my database")
    

@app.on_message(filters.private & filters.command("gc") & filters.user(OWNER_ID))
async def group_chats(client, message: Message):
    chats = await get_served_chats()
    if len(chats) == 0:
        await message.reply_text("no chat id found !")
        return
    await message.reply_text(f"{chats}")


@app.on_message(filters.private & filters.command("stats") & filters.user(OWNER_ID))
async def group_chats(client, message):
    chats = await get_served_chats()
    timev = await get_repeat_time()
    caption = f"""🥀 <u>**My Database Info:**</u> ✨
    
🌿 **Total Chats:** `{chats}`
🌷 **Delay Repeat Time Value:**
>> `{timev}` Seconds"""
    return await message.reply_text(caption)


@app.on_message(filters.private & filters.command('logs') & filters.user(OWNER_ID))
async def _get_logs(client, message: Message):
    if os.path.exists(LOG_FILE_NAME):
        x = await message.reply_text("🔄️ **ғᴇᴛᴄʜɪɴɢ ʟᴏɢs...**")
        await message.reply_document(LOG_FILE_NAME)
        await x.delete()
    else:
        await message.reply_text(f"⛔ **ʟᴏɢ ғɪʟᴇ `{LOG_FILE_NAME}` ᴅᴏᴇs ɴᴏᴛ ᴇxɪsᴛ.**")
