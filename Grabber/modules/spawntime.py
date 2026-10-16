from pyrogram import filters, enums
from Grabber import app
from Grabber.core.mongo import settingsdb
import config

@app.on_message(filters.command("changetime"))
async def change_time(_, message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    if message.chat.type == enums.ChatType.PRIVATE:
        return await message.reply_text("🛑 This command only works in groups.")

    # Bot Owner တစ်ယောက်တည်းသာ ပြောင်းနိုင်စေရန် စစ်ဆေးခြင်း
    if user_id not in config.OWNER_ID:
        return await message.reply_text("🛑 This command is only for the bot owner!")

    if len(message.command) < 2:
        return await message.reply_text(
            "❗ Usage:\n<code>/changetime count</code>\nExample: <code>/changetime 30</code>"
        )

    try:
        count = int(message.text.split(maxsplit=1)[1])
    except ValueError:
        return await message.reply_text("⚠️ Please enter a valid number. Example: <code>/changetime 30</code>")

    await settingsdb.change_spawn_time(chat_id, count)
    await message.reply_text(f"✅ Spawn time successfully set to <b>{count}</b> messages.")
