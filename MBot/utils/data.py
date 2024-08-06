from pyrogram.types import ReplyKeyboardMarkup, KeyboardButton, BotCommand

CONTACT_BUTTON = ReplyKeyboardMarkup([[KeyboardButton("Send Phone Number", request_contact=True)]], resize_keyboard=True)

BOT_COMMANDS = [
    BotCommand("start", "Start The Bot"),
    BotCommand("posting", "Enable/Disable Posting"),
    BotCommand("sm", "Set Message"),
    BotCommand("st", "Set Time"),
    BotCommand("delay", "Set Delay"),
    BotCommand("addchat", "Add Chat"),
    BotCommand("delchat", "Delete Chat"),
    BotCommand("gc", "Get Group Chats"),
    BotCommand("stats", "Get Stats"),
    BotCommand("logs", "Get Bot Logs"),
    BotCommand("help", "Help Command"),
    BotCommand("auth", "Connect Userbot")
]
