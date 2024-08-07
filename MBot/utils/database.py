from MBot import BOT_ID
from MBot.mongo import mongodb

# DB Collections
posting_col = mongodb.posting
textdb = mongodb.textdb
msgdb = mongodb.msgdb
limitdb = mongodb.limitdb
allowdb = mongodb.allowdb
chatsdb = mongodb.chatsdb
delaydb = mongodb.delaydb


# Repeater Bot On/Off
async def get_posting_mode() -> bool:
    on_off = await posting_col.find_one({})
    if on_off:
        posting = on_off["posting"]
        return posting
    return True


async def set_posting_mode(posting: bool) -> bool:
    posting_mode = await get_posting_mode()
    if posting == posting_mode:
        return False
    await posting_col.update_one(
        {"posting": posting_mode},
        {"$set": {"posting": posting}},
        upsert=True,
    )
    return True



# Custom Text
async def get_repeater_text() -> str:
    repeat_text = await textdb.find_one()
    if not repeat_text:
        return "Hello World"
    get_text = repeat_text["repeat_text"]
    return get_text


async def set_repeater_text(text: str) -> bool:
    get_text = await get_repeater_text()
    await textdb.update_one(
        {"repeat_text": get_text},
        {"$set": {"repeat_text": text}},
        upsert=True,
    )
    return True




async def get_post() -> int:
    post_doc = await msgdb.find_one({"_id": BOT_ID})
    if not post_doc:
        return 0
    return post_doc["message_id"]


async def set_post(message_id: int) -> bool:
    await msgdb.update_one(
        {"_id": BOT_ID},
        {"$set": {"message_id": message_id}},
        upsert=True,
    )
    return True



# PM Limit
async def get_repeat_time() -> int:
    limit = await limitdb.find_one()
    if not limit:
        return 120
    get_limit = limit["repeat_timer"]
    return get_limit


async def set_repeat_time(number: int) -> bool:
    get_limit = await get_repeat_time()
    if get_limit == number:
        return False
    await limitdb.update_one(
        {"repeat_timer": get_limit},
        {"$set": {"repeat_timer": number}},
        upsert=True,
    )
    return True



# chats
async def get_served_chats() -> list:
    chats_list = []
    async for chat in chatsdb.find({"chat_id": {"$lt": 0}}):
        chats_list.append(chat["chat_id"])
    return chats_list


async def is_served_chat(chat_id: int) -> bool:
    chat = await chatsdb.find_one({"chat_id": chat_id})
    if not chat:
        return False
    return True


async def add_served_chat(chat_id: int) -> bool:
    is_served = await is_served_chat(chat_id)
    if is_served:
        return False
    await chatsdb.insert_one({"chat_id": chat_id})
    return True


async def del_served_chat(chat_id: int) -> bool:
    is_served = await is_served_chat(chat_id)
    if not is_served:
        return False
    await chatsdb.delete_one({"chat_id": chat_id})
    return True


# allowed Users Database

async def is_allowed_user(user_id: int) -> bool:
    user = await allowdb.find_one({"user_id": user_id})
    if not user:
        return False
    return True


async def add_allowed_user(user_id: int) -> bool:
    is_approved = await is_allowed_user(user_id)
    if is_approved:
        return False
    await allowdb.insert_one({"user_id": user_id})
    return True


async def del_allowed_user(user_id: int) -> bool:
    is_approved = await is_allowed_user(user_id)
    if not is_approved:
        return False
    await allowdb.delete_one({"user_id": user_id})
    return True


async def get_allowed_users() -> list:
    approved_users_list = []
    async for user in allowdb.find({"user_id": {"$gt": 0}}):
        approved_users_list.append(user)
    return approved_users_list



# SET GROUP DELAY

async def get_delay_time() -> int:
    delay = await delaydb.find_one()
    if delay:
        get_delay = delay["delay_timer"]
        return int(get_delay)
    return 1


async def set_delay_time(number: int) -> bool:
    get_delay = await get_delay_time()
    if get_delay == number:
        return False
    await delaydb.update_one(
        {"delay_timer": get_delay},
        {"$set": {"delay_timer": number}},
        upsert=True,
    )
    return True
