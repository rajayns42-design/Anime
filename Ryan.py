import os
# --- CRITICAL FIX: MUST BE AT THE VERY TOP ---
os.environ["GIT_PYTHON_REFRESH"] = "quiet"
# ---------------------------------------------

from threading import Thread
from flask import Flask
from telegram import Update 
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler, 
    ChatMemberHandler, MessageHandler, filters
)
from telegram.request import HTTPXRequest

# --- INTERNAL IMPORTS ---
from baka.utils import track_group, log_to_channel, BOT_NAME
from baka.config import TOKEN, PORT

# --- IMPORT ALL PLUGINS ---
from baka.plugins import (
    start, economy, game, admin, broadcast, fun, events, 
    welcome, ping, chatbot, riddle, social, ai_media, 
    waifu, collection, shop, daily, 
    mafia, wordseek  # <--- WordSeek plugin yahan add kiya
)

# --- FLASK SERVER (Health Check) ---
app = Flask(__name__)

@app.route('/')
def health(): 
    return "Alive"

def run_flask(): 
    app.run(host='0.0.0.0', port=PORT, debug=False, use_reloader=False)

# --- STARTUP LOGIC ---
async def post_init(application):
    """Runs immediately after bot connects to Telegram."""
    print("✅ Bot connected! Setting menu commands...")

    # Menu commands updated with WordSeek
    await application.bot.set_my_commands([
        ("start", "🌸 Main Menu"), 
        ("word", "🎯 Start WordSeek Game"),
        ("hint", "💡 Get Word Hint (Limit 2/week)"),
        ("leaderboard", "🏆 WordSeek Ranking"),
        ("bal", "👛 Check Wallet"), 
        ("create_team", "🏢 Create Your Team"), 
        ("ranking", "🏆 Global Economy Ranking"), 
        ("daily", "📅 Daily Reward"),
        ("shop", "🛒 Item Shop"),
        ("ping", "📶 Status"),
        ("update", "🔄 Update Bot"),
    ])

    try:
        bot_info = await application.bot.get_me()
        print(f"✅ Logged in as {bot_info.username}")
    except Exception as e:
        print(f"⚠️ Startup Log Failed: {e}")

# --- MAIN EXECUTION ---
if __name__ == '__main__':
    flask_thread = Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()

    if not TOKEN:
        print("CRITICAL: BOT_TOKEN is missing.")
    else:
        t_request = HTTPXRequest(connection_pool_size=16, connect_timeout=60.0, read_timeout=60.0)
        app_bot = ApplicationBuilder().token(TOKEN).request(t_request).post_init(post_init).build()

        # ================= REGISTER HANDLERS =================

        # --- 1. Basics & Start ---
        app_bot.add_handler(CommandHandler("start", start.start))
        app_bot.add_handler(CommandHandler("help", start.help_command))
        app_bot.add_handler(CommandHandler("ping", ping.ping))
        app_bot.add_handler(CallbackQueryHandler(ping.ping_callback, pattern="^sys_stats$"))
        app_bot.add_handler(CallbackQueryHandler(start.help_callback, pattern="^help_"))

        # --- 2. Economy & Shop ---
        app_bot.add_handler(CommandHandler("bal", economy.balance))
        app_bot.add_handler(CommandHandler("ranking", economy.ranking))
        app_bot.add_handler(CommandHandler("give", economy.give))
        app_bot.add_handler(CommandHandler("daily", daily.daily))
        app_bot.add_handler(CommandHandler("shop", shop.shop_menu))
        app_bot.add_handler(CommandHandler("buy", shop.buy))

        # --- 3. 🕶️ MAFIA / TEAM SYSTEM ---
        app_bot.add_handler(CommandHandler("create_team", mafia.create_team))
        app_bot.add_handler(CommandHandler("join_team", mafia.join_team))
        app_bot.add_handler(CommandHandler("team_war", mafia.team_war))
        app_bot.add_handler(CommandHandler("arena", mafia.arena_fight))

        # --- 4. 🎯 WORDSEEK GAME (New Integration) ---
        app_bot.add_handler(CommandHandler("word", wordseek.start_game))
        app_bot.add_handler(CommandHandler("hint", wordseek.get_hint))
        app_bot.add_handler(CommandHandler("leaderboard", wordseek.leaderboard))

        # --- 5. RPG Game ---
        app_bot.add_handler(CommandHandler("kill", game.kill))
        app_bot.add_handler(CommandHandler("rob", game.rob))

        # --- 6. Admin & System ---
        app_bot.add_handler(CommandHandler("broadcast", broadcast.broadcast))
        app_bot.add_handler(CommandHandler("addcoins", admin.addcoins))
        app_bot.add_handler(CommandHandler("update", admin.update_bot))

        # --- 7. EVENTS & LISTENERS ---
        app_bot.add_handler(ChatMemberHandler(events.chat_member_update, ChatMemberHandler.MY_CHAT_MEMBER))
        app_bot.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome.new_member))
        
        # WordSeek Guess Listener (Group 3 mein rakha hai taaki Chatbot se pehle check ho)
        app_bot.add_handler(MessageHandler(filters.TEXT & filters.ChatType.GROUPS & ~filters.COMMAND, wordseek.guess), group=3)
        
        # Baaki listeners
        app_bot.add_handler(MessageHandler(filters.TEXT & filters.ChatType.GROUPS & ~filters.COMMAND, collection.collect_waifu), group=1)
        app_bot.add_handler(MessageHandler((filters.TEXT | filters.Sticker.ALL) & ~filters.COMMAND, chatbot.ai_message_handler), group=4)
        app_bot.add_handler(MessageHandler(filters.ChatType.GROUPS, events.group_tracker), group=5)

        print("🚀 ZEXX Angel Bot is LIVE!")
        app_bot.run_polling(allowed_updates=Update.ALL_TYPES, drop_pending_updates=True)
