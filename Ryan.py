# --- SYSTEM FIX ---
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

# --- INTERNAL UTILS ---
from baka.utils import track_group, log_to_channel, BOT_NAME
from baka.config import TOKEN, PORT

# --- ALL PLUGINS SYNCED (AK BHI NAHI CHHUTA) ---
from baka.plugins import (
    start, economy, game, admin, broadcast, fun, events,
    welcome, ping, chatbot, riddle, social, ai_media,
    waifu, collection, shop, daily,
    mafia, wordseek
)

# ---------------- FLASK (Stay Alive) ----------------
app = Flask(__name__)
@app.route('/')
def health(): return "Zexx Bot is Alive!"
def run_flask(): app.run(host='0.0.0.0', port=PORT, debug=False, use_reloader=False)

# ---------------- COMMAND MENU ----------------
async def post_init(application):
    await application.bot.set_my_commands([
        ("start", "Main Menu"),
        ("bal", "Wallet & Gold"),
        ("daily", "Claim Reward"),
        ("word", "WordSeek Game"),
        ("mafia", "Mafia Menu"),
        ("create_team", "Create Team"),
        ("team_war", "Mafia War"),
        ("riddle", "AI Riddle"),
        ("couple", "Match Making"),
        ("wpropose", "Waifu Marriage"),
        ("shop", "Item Shop")
    ])

# ---------------- THE MASTER MAIN ----------------
if __name__ == '__main__':
    Thread(target=run_flask, daemon=True).start()

    request = HTTPXRequest(connection_pool_size=20)
    app_bot = ApplicationBuilder().token(TOKEN).request(request).post_init(post_init).build()

    # ========= 1. SYSTEM & ADMIN (Core) =========
    app_bot.add_handler(CommandHandler("start", start.start))
    app_bot.add_handler(CommandHandler("ping", ping.ping))
    app_bot.add_handler(CommandHandler("help", start.start))
    app_bot.add_handler(CommandHandler("update", admin.update_bot))
    app_bot.add_handler(CommandHandler("broadcast", broadcast.broadcast))

    # ========= 2. ECONOMY & REWARDS (Zexx Style) =========
    app_bot.add_handler(CommandHandler("bal", economy.balance))
    app_bot.add_handler(CommandHandler("ranking", economy.ranking))
    app_bot.add_handler(CommandHandler("daily", daily.daily))
    app_bot.add_handler(CommandHandler("give", economy.give))
    app_bot.add_handler(CommandHandler("shop", shop.shop_menu))
    app_bot.add_handler(CommandHandler("buy", shop.buy))

    # ========= 3. MAFIA & ACTION RPG =========
    app_bot.add_handler(CommandHandler("create_team", mafia.create_team))
    app_bot.add_handler(CommandHandler("join_team", mafia.join_team))
    app_bot.add_handler(CommandHandler("mpromote", mafia.promote_member))
    app_bot.add_handler(CommandHandler("leave_team", mafia.leave_team))
    app_bot.add_handler(CommandHandler("team_war", mafia.team_war))
    app_bot.add_handler(CommandHandler("t_deposit", mafia.team_deposit))
    app_bot.add_handler(CommandHandler("t_lb", mafia.team_leaderboard))
    app_bot.add_handler(CommandHandler("arena", mafia.arena_fight))
    app_bot.add_handler(CommandHandler("kill", game.kill))
    app_bot.add_handler(CommandHandler("rob", game.rob))
    app_bot.add_handler(CommandHandler("protect", game.protect))

    # ========= 4. WAIFU & SOCIAL (Relationship Logic) =========
    app_bot.add_handler(CommandHandler("wpropose", waifu.wpropose))
    app_bot.add_handler(CommandHandler("wmarry", waifu.wmarry))
    app_bot.add_handler(CommandHandler("couple", social.couple_game))
    app_bot.add_handler(CommandHandler("propose", social.propose))
    app_bot.add_handler(CommandHandler("divorce", social.divorce))
    # SFW Actions (kiss, slap, hug, etc.)
    for action in waifu.SFW_ACTIONS:
        app_bot.add_handler(CommandHandler(action, waifu.waifu_action))

    # ========= 5. FUN & GAMES =========
    app_bot.add_handler(CommandHandler("word", wordseek.start_game))
    app_bot.add_handler(CommandHandler("hint", wordseek.get_hint))
    app_bot.add_handler(CommandHandler("wlb", wordseek.leaderboard))
    app_bot.add_handler(CommandHandler("riddle", riddle.riddle_command))
    
      
    # 🎲 THE DICE HANDLER (Fixed for Crash)
    app_bot.add_handler(CommandHandler("dice", fun.dice)) 
    
   
    app_bot.add_handler(CommandHandler("speak", ai_media.speak_command))
    app_bot.add_handler(CommandHandler("draw", ai_media.draw_command))

    # ========= 6. SYSTEM CALLBACKS =========
    app_bot.add_handler(CallbackQueryHandler(start.menu_callback, pattern="^start_"))
    app_bot.add_handler(CallbackQueryHandler(shop.shop_callback, pattern="^shop_"))
    app_bot.add_handler(CallbackQueryHandler(social.proposal_callback, pattern="^marry_"))

    # ========= 7. MESSAGE LISTENERS (Strict Priority) =========
    # P0: WordSeek (Fast Guessing)
    app_bot.add_handler(MessageHandler(filters.TEXT & filters.ChatType.GROUPS & ~filters.COMMAND, wordseek.guess), group=0)
    # P1: Group Stats & Auto-Add
    app_bot.add_handler(MessageHandler(filters.ChatType.GROUPS, events.group_tracker), group=1)
    # P2: Waifu Drops (Har 100 msg ke baad)
    app_bot.add_handler(MessageHandler(filters.TEXT & filters.ChatType.GROUPS & ~filters.COMMAND, collection.check_drops), group=2)
    app_bot.add_handler(MessageHandler(filters.TEXT & filters.ChatType.GROUPS & ~filters.COMMAND, collection.collect_waifu), group=3)
    # P4: Riddle Answer
    app_bot.add_handler(MessageHandler(filters.TEXT & filters.ChatType.GROUPS & ~filters.COMMAND, riddle.check_riddle_answer), group=4)
    # P5: Chatbot Learning & AI Reply
    app_bot.add_handler(MessageHandler((filters.TEXT | filters.Sticker.ALL) & ~filters.COMMAND, chatbot.ai_message_handler), group=5)

    # ========= 8. LOGS & EVENTS =========
    app_bot.add_handler(ChatMemberHandler(events.chat_member_update))
    app_bot.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome.new_member))

    print(f"✅ {BOT_NAME} ZEXX FINAL EDITION IS NOW FULLY OPERATIONAL!")
    app_bot.run_polling(allowed_updates=Update.ALL_TYPES, drop_pending_updates=True)
