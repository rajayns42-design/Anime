import random
from telethon import events # Agar aap Telethon use kar rahe hain
# Pyrogram ke liye: from pyrogram import filters

# ===============================================
# DATABASE LOGIC (REFIXED)
# ===============================================

def is_chatbot_enabled(chat_id):
    # Chat ID ko string mein convert karna best hai compatibility ke liye
    doc = chatbot_collection.find_one({"chat_id": str(chat_id)})
    if doc:
        return doc.get("enabled", True) # By default ON rahega
    return True

def get_chat_response(word):
    # Word ko lowercase karke search karein
    data = chatbot_collection.find_one({"word": word.lower().strip()})
    if data and "responses" in data:
        return random.choice(data["responses"]) # Ek random reply select karega
    return None

# ===============================================
# MAIN HANDLER (PRIVATE & GROUP BOTH)
# ===============================================

@bot.on(events.NewMessage)
async def chatbot_logic(event):
    # 1. Message ka text aur chat_id nikaalein
    message_text = event.raw_text.lower().strip()
    chat_id = event.chat_id

    # 2. Commands check karein (ON/OFF karne ke liye)
    if message_text == "/chatbot on":
        toggle_chatbot_status(chat_id, True)
        await event.reply("✅ Chatbot is now **ON** for this chat.")
        return
    elif message_text == "/chatbot off":
        toggle_chatbot_status(chat_id, False)
        await event.reply("❌ Chatbot is now **OFF** for this chat.")
        return

    # 3. Agar Chatbot Enable hai, toh reply check karein
    if is_chatbot_enabled(chat_id):
        # Database se reply dhoondein
        reply = get_chat_response(message_text)
        
        if reply:
            await event.reply(reply)

# ===============================================
# ADDING WORDS (TAAKI BOT KUCH SEEKHE)
# ===============================================

@bot.on(events.NewMessage(pattern="/addchat (.+)"))
async def add_chat(event):
    input_str = event.pattern_match.group(1)
    if "|" in input_str:
        word, response = input_str.split("|", 1)
        add_chat_to_db(word, response)
        await event.reply(f"Done! Jab koi `{word.strip()}` bolega, main `{response.strip()}` kahunga.")
    else:
        await event.reply("Sahi format use karein: `/addchat hello | namaste`")
