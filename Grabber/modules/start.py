import motor, sys, time
from Grabber import app
from config import OWNER_ID
from pyrogram import filters, enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from Grabber.core.mongo import usersdb, waifusdb, chatsdb

# --------------------------------------- Chat Watcher --------------------------------------- #

start_time = time.time()

@app.on_message(group=10)
async def chat_watcher_func(_, message):
    try:
        # ---------------- User Save ---------------- #
        if message.from_user:
            user_id = message.from_user.id
            if not await usersdb.is_user_exist(user_id):
                await usersdb.add_user(user_id)

        # ---------------- Chat Save ---------------- #
        if message.chat:
            chat_id = message.chat.id
            if not await chatsdb.is_chat_exist(chat_id):
                await chatsdb.add_chat(chat_id)
    except Exception:
        pass


# --------------------------------------- Bot Running Time --------------------------------------- #

def time_formatter():
    minutes, seconds = divmod(int(time.time() - start_time), 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    weeks, days = divmod(days, 7)
    tmp = (
        ((str(weeks) + "w:") if weeks else "")
        + ((str(days) + "d:") if days else "")
        + ((str(hours) + "h:") if hours else "")
        + ((str(minutes) + "m:") if minutes else "")
        + ((str(seconds) + "s") if seconds else "")
    )
    if tmp != "":
        if tmp.endswith(":"):
            return tmp[:-1]
        else:
            return tmp
    else:
        return "0 s"


# --------------------------------------- Start Command --------------------------------------- #

@app.on_message(filters.command("start"))
async def start(client, message):
    # ခလုတ်တစ်ခုချင်းစီ သီးသန့်စီ အတန်းလိုက် ပေါ်စေရန် အကွက်အကွင်း မှန်ကန်စွာ ဖန်တီးထားခြင်း
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("➕ Add Me To Your Group", url=f"https://t.me/{client.me.username}?startgroup=true")
        ],
        [
            InlineKeyboardButton("✨ Support", url="https://t.me/Social_IT_Service"),
            InlineKeyboardButton("📖 Guide", url="https://t.me/Social_IT_Service")
        ],
        [
            InlineKeyboardButton("💬 Contact Owner", url="https://t.me/Social_IT_Service")
        ]
    ])

    await message.reply_text(
        f"""
Hello {message.from_user.mention} !

I’m **{(await client.get_me()).mention}**. Every grab could unlock a rare waifu from the anime multiverse. Build your collection, trade smart, and rise through the ranks. Your journey to becoming the ultimate collector starts now.
        """,
        reply_markup=keyboard
    )


# --------------------------------------- Stats Command --------------------------------------- #

@app.on_message(filters.command("stats") & filters.user(OWNER_ID))
async def stats(client, message):
    start = time.time()
    users = len(await usersdb.get_all_users())
    chats = len(await chatsdb.get_all_chats())
    waifus = len(await waifusdb.getAllWaifus())
    ping = round((time.time() - start) * 1000)
    await message.reply_text(f"""
**Stats of** {(await client.get_me()).mention} :

🏓 **Ping Pong**: {ping}ms
📊 **Total Users** : `{users}`
🌼 **Total Chats**: `{chats}`
💮 **Total Waifus**: `{waifus}`
⚙️ **Bot Uptime** : `{time_formatter()}`
    
🎨 **Python Version**: `{sys.version.split()[0]}`
📑 **Mongo Version**: `{motor.version}`
""")
