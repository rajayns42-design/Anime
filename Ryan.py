# --- CRITICAL FIX ---
import os
os.environ["GIT_PYTHON_REFRESH"] = "quiet"

from threading import Thread
from flask import Flask
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler,
    ChatMemberHandler, MessageHandler, filters
)
from telegram.request import HTTPXRequest

# --- INTERNAL ---
from baka.utils import track_group, log_to_channel, BOT_NAME
from baka.config import TOKEN, PORT

# --- ALL PLUGINS IMPORT ---
from baka.plugins import (
    start, economy, game, admin, broadcast, fun, events,
    welcome, ping, chatbot, riddle, social, ai_media,
    waifu, collection, shop, daily,
    mafia, wordseek
)

# ---------------- FLASK ----------------
app = Flask(__name__)
@app.route('/')
def health(): return "Alive"
def run_flask(): app.run(host='0.0.0.0', port=PORT, debug=False, use_reloader=False)

# ---------------- POST INIT ----------------
async def post_init(application):
    await application.bot.set_my_commands([
        ("start", "Main Menu"),
        ("help", "Command Diary"),
        ("bal", "Wallet & Rank"),
        ("daily", "Daily Reward"),
        ("shop", "Item Shop"),
        ("ranking", "Global Leaderboard"),
        ("word", "WordSeek Unlimited"),
        ("addchat", "Bulk Add Chatbot"),
        ("draw", "AI Art Generation"),
        ("marry", "Check Relationship Status"),
    ])

# ---------------- MAIN ----------------
if __name__ == '__main__':
    Thread(target=run_flask, daemon=True).start()

    request = HTTPXRequest(connection_pool_size=20)
    app_bot = ApplicationBuilder().token(TOKEN).request(request).post_init(post_init).build()

    # ========= 1. BASIC & MENU =========
    app_bot.add_handler(CommandHandler("start", start.start))
    app_bot.add_handler(CommandHandler("help", start.start))
    app_bot.add_handler(CommandHandler("ping", ping.ping))
    app_bot.add_handler(CommandHandler("update", admin.update_bot))

    # ========= 2. ECONOMY & REWARDS (From Screenshots) =========
    app_bot.add_handler(CommandHandler("bal", economy.balance))
    app_bot.add_handler(CommandHandler("daily", daily.daily))
    app_bot.add_handler(CommandHandler("shop", shop.shop_menu))
    app_bot.add_handler(CommandHandler("ranking", economy.leaderboard))
    app_bot.add_handler(CommandHandler("give", economy.transfer))
    app_bot.add_handler(CommandHandler("claim", economy.claim_bonus))

    # ========= 3. MURDER & STEAL (Action Games) =========
    app_bot.add_handler(CommandHandler("kill", game.kill))
    app_bot.add_handler(CommandHandler("rob", game.rob))
    app_bot.add_handler(CommandHandler("revive", game.revive))
    app_bot.add_handler(CommandHandler("protect", shop.buy_immunity))

    # ========= 4. WORDSEEK (Unlimited Loop) =========
    app_bot.add_handler(CommandHandler("word", wordseek.start_game))
    app_bot.add_handler(CommandHandler("hint", wordseek.get_hint))
    app_bot.add_handler(CommandHandler("leaderboard", wordseek.leaderboard))

    # ========= 5. RELATIONSHIPS (Waifu & Marry) =========
    app_bot.add_handler(CommandHandler("couple", social.match_maker))
    app_bot.add_handler(CommandHandler("marry", social.check_status))
    app_bot.add_handler(CommandHandler("propose", social.propose))
    app_bot.add_handler(CommandHandler("divorce", social.break_up))
    app_bot.add_handler(CommandHandler("wpropose", waifu.propose))
    app_bot.add_handler(CommandHandler("wmarry", waifu.random_marry))

    # ========= 6. AI & MEDIA =========
    app_bot.add_handler(CommandHandler("draw", ai_media.generate))
    app_bot.add_handler(CommandHandler("speak", ai_media.voice))
    app_bot.add_handler(CommandHandler("chatbot", chatbot.settings)) # AI Settings
    app_bot.add_handler(CommandHandler("addchat", chatbot.add_chat_handler)) # Bulk Add

    # ========= 7. FUN & GAMES =========
    app_bot.add_handler(CommandHandler("dice", fun.roll)) # Gamble
    app_bot.add_handler(CommandHandler("riddle", riddle.riddle))
    app_bot.add_handler(CommandHandler("answer", riddle.answer))

    # ========= 8. MAFIA SYSTEM =========
    app_bot.add_handler(CommandHandler("create_team", mafia.create_team))
    app_bot.add_handler(CommandHandler("join_team", mafia.join_team))
    app_bot.add_handler(CommandHandler("team_war", mafia.team_war))
    app_bot.add_handler(CommandHandler("team_leaderboard", mafia.team_leaderboard))

    # ========= 9. CALLBACKS & LISTENERS =========
    app_bot.add_handler(CallbackQueryHandler(start.menu_callback))

    # MESSAGE LISTENERS (Priority Based)
    # Group 0: WordSeek Guess (Sabse pehle check hoga)
    app_bot.add_handler(MessageHandler(filters.TEXT & filters.ChatType.GROUPS & ~filters.COMMAND, wordseek.guess), group=0)
    
    # Group 1: Waifu Collection
    app_bot.add_handler(MessageHandler(filters.TEXT & filters.ChatType.GROUPS & ~filters.COMMAND, collection.collect_waifu), group=1)

    # Group 5: Chatbot AI (Replies to text/stickers)
    app_bot.add_handler(MessageHandler((filters.TEXT | filters.Sticker.ALL) & ~filters.COMMAND, chatbot.ai_message_handler), group=5)

    # ========= 10. EVENTS =========
    app_bot.add_handler(ChatMemberHandler(events.chat_member_update))
    app_bot.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome.new_member))
    app_bot.add_handler(MessageHandler(filters.ChatType.GROUPS, events.group_tracker), group=10)

    print(f"✅ {BOT_NAME} ZEXX EDITION: ALL COMMANDS INTEGRATED SUCCESSFULLY!")
    
    app_bot.run_polling(allowed_updates=Update.ALL_TYPES, drop_pending_updates=True)
