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
        ("word", "WordSeek Unlimited"),
        ("addchat", "Bulk Add Chatbot"),
        ("mafia", "Mafia Menu"),
        ("mpromote", "Mafia Promote"),
    ])

# ---------------- MAIN ----------------
if __name__ == '__main__':
    Thread(target=run_flask, daemon=True).start()

    request = HTTPXRequest(connection_pool_size=20)
    app_bot = ApplicationBuilder().token(TOKEN).request(request).post_init(post_init).build()

    # ========= 1. BASIC & CORE =========
    app_bot.add_handler(CommandHandler("start", start.start))
    app_bot.add_handler(CommandHandler("help", start.start))
    app_bot.add_handler(CommandHandler("ping", ping.ping))
    app_bot.add_handler(CommandHandler("update", admin.update_bot))

    # ========= 2. ECONOMY (FIXED) =========
    app_bot.add_handler(CommandHandler("bal", economy.balance))
    app_bot.add_handler(CommandHandler("daily", daily.daily))
    app_bot.add_handler(CommandHandler("shop", shop.shop_menu))
    # CRITICAL FIX: leaderboard -> ranking (as per your economy.py)
    app_bot.add_handler(CommandHandler("ranking", economy.ranking)) 
    # CRITICAL FIX: transfer -> give (as per your economy.py)
    app_bot.add_handler(CommandHandler("give", economy.give)) 
    app_bot.add_handler(CommandHandler("claim", economy.claim))

    # ========= 3. ACTION & MURDER =========
    app_bot.add_handler(CommandHandler("kill", game.kill))
    app_bot.add_handler(CommandHandler("rob", game.rob))
    app_bot.add_handler(CommandHandler("revive", game.revive))
    app_bot.add_handler(CommandHandler("protect", shop.buy_immunity))

    # ========= 4. MAFIA SYSTEM (ZEXX Edition) =========
    app_bot.add_handler(CommandHandler("mafia", mafia.mafia_menu))
    app_bot.add_handler(CommandHandler("create_team", mafia.create_team))
    app_bot.add_handler(CommandHandler("join_team", mafia.join_team))
    # Mafia Promote Handler
    app_bot.add_handler(CommandHandler("mpromote", mafia.promote_member)) 
    app_bot.add_handler(CommandHandler("team_war", mafia.team_war))
    app_bot.add_handler(CommandHandler("team_leaderboard", mafia.team_leaderboard))

    # ========= 5. WORDSEEK (Unlimited Loop) =========
    app_bot.add_handler(CommandHandler("word", wordseek.start_game))
    app_bot.add_handler(CommandHandler("hint", wordseek.get_hint))

    # ========= 6. RELATIONSHIPS =========
    app_bot.add_handler(CommandHandler("couple", social.match_maker))
    app_bot.add_handler(CommandHandler("marry", social.check_status))
    app_bot.add_handler(CommandHandler("propose", social.propose))
    app_bot.add_handler(CommandHandler("divorce", social.break_up))

    # ========= 7. AI & CHATBOT TOOLS =========
    app_bot.add_handler(CommandHandler("draw", ai_media.generate))
    app_bot.add_handler(CommandHandler("speak", ai_media.voice))
    # Bulk AddChat Handler
    app_bot.add_handler(CommandHandler("addchat", chatbot.add_chat_handler)) 

    # ========= 8. FUN & GAMES =========
    app_bot.add_handler(CommandHandler("dice", fun.roll))
    app_bot.add_handler(CommandHandler("roll", fun.roll))

    # ========= 9. CALLBACKS & LISTENERS =========
    app_bot.add_handler(CallbackQueryHandler(start.menu_callback))

    # Message Listeners with Priority Groups
    app_bot.add_handler(MessageHandler(filters.TEXT & filters.ChatType.GROUPS & ~filters.COMMAND, wordseek.guess), group=0)
    app_bot.add_handler(MessageHandler((filters.TEXT | filters.Sticker.ALL) & ~filters.COMMAND, chatbot.ai_message_handler), group=5)

    # ========= 10. EVENTS =========
    app_bot.add_handler(ChatMemberHandler(events.chat_member_update))
    app_bot.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome.new_member))

    print(f"✅ {BOT_NAME} FINAL FIX LOADED: NO MORE CRASHES!")
    
    app_bot.run_polling(allowed_updates=Update.ALL_TYPES, drop_pending_updates=True)
