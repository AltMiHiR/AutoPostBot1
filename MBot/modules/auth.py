from config import API_ID, API_HASH, OWNER_ID

from sqlite3 import OperationalError
from pyromod.exceptions import ListenerTimeout

from pyrogram import Client, filters
from pyrogram.types import ReplyKeyboardRemove, Message
from pyrogram.errors import PhoneNumberInvalid, PhoneCodeInvalid, PhoneCodeExpired, SessionPasswordNeeded, PasswordHashInvalid, PhonePasswordFlood

from MBot import MBot, BOT_ID, app
from MBot.utils.data import CONTACT_BUTTON
from MBot.utils.userbot import userbots_col


@app.on_message(filters.private & filters.command("auth") & filters.user(OWNER_ID))
async def _authorize(bot: MBot, message: Message):
    user_id = message.chat.id

    phone_message = """Now Tap on `Send Phone Number` button to send your this Account's phone number.
**OR**
Send your Telegram Account's `PHONE_NUMBER` in International Format, Including Country code.
Example : +911234567890"""
    try:
        phone_number_msg = await bot.ask(user_id, phone_message, reply_markup=CONTACT_BUTTON, timeout=60)
    except ListenerTimeout:
        await message.reply_text('⚠️ **ᴛɪᴍᴇᴅ ᴏᴜᴛ.**', reply_markup=ReplyKeyboardRemove())
        return

    if phone_number_msg.text:
        if "/cancel" in phone_number_msg.text:
            await message.reply_text("⛔ **ᴄᴀɴᴄᴇʟʟᴇᴅ ᴛʜᴇ ᴘʀᴏᴄᴇss.**", reply_markup=ReplyKeyboardRemove())
            return
        phone_number = phone_number_msg.text
    elif phone_number_msg.contact:
        phone_number = "+" + phone_number_msg.contact.phone_number
    else:
        await message.reply_text("⚠️ **ɪɴᴠᴀʟɪᴅ ᴘʜᴏɴᴇ_ɴᴜᴍʙᴇʀ.**", reply_markup=ReplyKeyboardRemove())
        return

    otpx_message = await message.reply_text("🔄️ **sᴇɴᴅɪɴɢ ᴏᴛᴘ...**", reply_markup=ReplyKeyboardRemove())
    account = Client("Userbot", api_id=API_ID, api_hash=API_HASH, in_memory=True, no_updates=True)

    try:
        await account.connect()
        code = await account.send_code(phone_number)
    except OperationalError:
        await message.reply_text('⛔ **ғᴀɪʟᴇᴅ ᴛᴏ ᴄᴏɴɴᴇᴄᴛ ᴀᴄᴄᴏᴜɴᴛ.**\n\nᴘʟᴇᴀsᴇ ᴛʀʏ ᴀɢᴀɪɴ.')
        return
    except PhoneNumberInvalid:
        await message.reply_text('⚠️ **ɪɴᴠᴀʟɪᴅ ᴘʜᴏɴᴇ_ɴᴜᴍʙᴇʀ.**')
        return
    except PhonePasswordFlood:
        await message.reply_text('⚠️ **ʏᴏᴜ ʜᴀᴠᴇ ᴛʀɪᴇᴅ ʟᴏɢɢɪɴɢ ɪɴ ᴛᴏᴏ ᴍᴀɴʏ ᴛɪᴍᴇs.**\n\nᴛʀʏ ᴀɢᴀɪɴ ᴀғᴛᴇʀ sᴏᴍᴇ ᴛɪᴍᴇ.')
        return
    finally:
        try:
            await otpx_message.delete()
        except:
            pass

    try:
        phone_code_msg = await bot.ask(user_id, "**An OTP is sent to your Telegram App.**\n\n⚠ Please enter OTP in `1 2 3 4 5` format.\n\nEnter /cancel to Cancel Process.", filters=filters.text, timeout=60)
        if "/cancel" in phone_code_msg.text:
            await message.reply_text("⛔ **ᴄᴀɴᴄᴇʟʟᴇᴅ ᴛʜᴇ ᴘʀᴏᴄᴇss.**")
            return
    except ListenerTimeout:
        await message.reply_text('⚠️ **ᴛɪᴍᴇᴅ ᴏᴜᴛ.**')
        return

    try:
        await account.sign_in(phone_number, code.phone_code_hash, phone_code_msg.text)
        password = None
    except PhoneCodeInvalid:
        await message.reply_text('⚠️ **ᴏᴛᴘ ɪs ɪɴᴠᴀʟɪᴅ.**')
        return
    except PhoneCodeExpired:
        await message.reply_text('⚠️ **ᴏᴛᴘ ɪs ᴇxᴘɪʀᴇᴅ.**')
        return
    except SessionPasswordNeeded:
        try:
            two_step_msg = await bot.ask(user_id, '⚠️ **ʏᴏᴜʀ ᴀᴄᴄᴏᴜɴᴛ ʜᴀs ᴇɴᴀʙʟᴇᴅ ᴛᴡᴏ-sᴛᴇᴘ ᴠᴇʀɪғɪᴄᴀᴛɪᴏɴ.**\nᴘʟᴇᴀsᴇ ᴇɴᴛᴇʀ ᴛʜᴇ ᴘᴀssᴡᴏʀᴅ.\n\nᴇɴᴛᴇʀ /cancel ᴛᴏ ᴄᴀɴᴄᴇʟ ᴘʀᴏᴄᴇss.', filters=filters.text, timeout=60)
        except ListenerTimeout:
            await message.reply_text('⚠️ **ᴛɪᴍᴇᴅ ᴏᴜᴛ.**')
            return
        if "/cancel" in two_step_msg.text:
            await message.reply_text("⛔ **ᴄᴀɴᴄᴇʟʟᴇᴅ ᴛʜᴇ ᴘʀᴏᴄᴇss.**")
            return
        try:
            password = two_step_msg.text
            await account.check_password(password=password)
        except PasswordHashInvalid:
            await message.reply_text('⚠️ **ɪɴᴠᴀʟɪᴅ ᴘᴀssᴡᴏʀᴅ ᴇɴᴛᴇʀᴇᴅ.**')
            return

    try:
        await account.join_chat("TheAltron")
    except:
        pass
    try:
        await account.join_chat("AltronBots")
    except:
        pass

    string_session = await account.export_session_string()
    me = await account.get_me()
    phone_number = f"+{me.phone_number}"
    account_data = {"session": string_session, "phone_number": phone_number}
    if me.is_premium:
        account_data["is_premium"] = True
    await userbots_col.update_one({"_id": BOT_ID}, {"$set": account_data},upsert=True)

    await message.reply_text(f"✅ **sᴜᴄᴄᴇssғᴜʟʟʏ ᴀᴜᴛʜᴏʀɪᴢᴇᴅ.**")

    try:
        await account.disconnect()
    except:
        pass
