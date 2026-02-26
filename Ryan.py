# Copyright (c) 2025 Telegram:- @WTF_Phantom <DevixOP>
# Location: Supaul, Bihar 
#
# All rights reserved.
#
# This code is the intellectual property of @WTF_Phantom.
# You are not allowed to copy, modify, redistribute, or use this
# code for commercial or personal projects without explicit permission.
# Allowed:
# - Forking for personal learning
# - Submitting improvements via pull requests
# Not Allowed:
# - Claiming this code as your own
# - Re-uploading without credit or permission
# - Selling or using commercially
#
# Contact for permissions:
# Email: king25258069@gmail.com

import os
# --- CRITICAL FIX: MUST BE AT THE VERY TOP ---
# This prevents Heroku crashing due to Git/Path issues

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
from baka.config import TOKEN, PORT
from baka.utils import track_group, log_to_channel, BOT_NAME

# --- ALL PLUGINS SYNCED ---
from baka.plugins import (
    start, economy, game, admin, broadcast, fun, events,
    welcome, ping, chatbot, riddle, social, ai_media,
    waifu, collection, shop, daily,
    mafia, wordseek, wishes, couple, love, battle
)


# --- FLASK SERVER (Health Check) ---
app = Flask(__name__)

@app.route('/')
def health(): 
    return "Alive"

def run_flask(): 
    # Run on 0.0.0.0 to bind to Heroku's external port
    app.run(host='0.0.0.0', port=PORT, debug=False, use_reloader=False)

# --- STARTUP LOGIC ---
async def post_init(application):
    """Runs immediately after bot connects to Telegram."""
    print("✅ Bot connected! Setting menu commands...")
        BotCommand("start", "Tᴀʟᴋᴇ Tᴏ Aɴɢᴇʟ"),
        BotCommand("ping", "Cʜᴇᴋ ʏᴏᴜʀ Aɴɢᴇʟ Sᴩᴇᴇᴅ"),
        BotCommand("help", "Aɴɢᴇʟ Hᴇʟᴩ Mᴇɴᴜ"),
        BotCommand("bal", "Yᴏᴜʀ Wᴀʟʟᴇᴛ"),
        BotCommand("daily", "Aɴɢᴇʟ Dᴀɪʟʏ Rᴇᴡᴀʀᴅ"),
        BotCommand("shop", "Aɴɢᴇʟ Sʜᴏᴩ Mᴇɴᴜ"),
        BotCommand("pay", "Sᴇɴᴅ Fʀɪᴇᴅꜱ Mᴏɴᴇʏ"),
        BotCommand("kill", "Kɪʟʟ Yᴏᴜʀ ᴀɴʏᴏɴᴇ"),
        BotCommand("rob", "Rᴏʙ To Soᴍᴇᴏɴᴇ"),
        BotCommand("chatbot", "Aɴɢᴇʟ Aɪ Sᴇᴛᴛɪɴɢꜱ"),
        BotCommand("ask", "Aꜱᴋ Aɴʏᴛʜɪᴋ"),
        BotCommand("welcome", "Wᴇʟᴄᴏᴍᴇ Oɴ/Oғғ"),
        BotCommand("truth", "Fᴜɴ Wɪᴛʜ Lᴏᴠᴇ Tʀᴜᴛʜ"),
        BotCommand("dare", "Fᴜɴ Wɪᴛʜ Lᴏᴠᴇ Dᴀʀᴇ"),
        BotCommand("quiz", "Fᴜɴ Wɪᴛʜ Lᴏᴠᴇ Qᴜɪᴢ"),
        BotCommand("mafialb", "M-Lᴇᴀᴅᴇʀʙᴏᴀʀᴅ"),
        BotCommand("arena", "Pʟᴀʏ ᴛʜᴇ Aʀᴇɴᴀ"),
    
    # Logger: Jab bot Heroku par start hoga
    await log_to_channel(application.bot, "start") 

# ---------------- THE MASTER MAIN ----------------
if __name__ == '__main__':
    Thread(target=run_flask, daemon=True).start()

    request = HTTPXRequest(connection_pool_size=20)
    app_bot = ApplicationBuilder().token(TOKEN).request(request).post_init(post_init).build()

    # ========= 1. CORE & ADMIN (Logger Linked) =========
    app_bot.add_handler(CommandHandler("start", start.start))
    app_bot.add_handler(CommandHandler("ping", ping.ping))
    app_bot.add_handler(CommandHandler("help", start.start))
    app_bot.add_handler(CommandHandler("update", admin.update_bot))
    app_bot.add_handler(CommandHandler("broadcast", broadcast.broadcast))

    # ========= 2. ECONOMY & WITHDRAWALS =========
    app_bot.add_handler(CommandHandler("bal", economy.balance))
    app_bot.add_handler(CommandHandler("top", economy.ranking))
    app_bot.add_handler(CommandHandler("daily", daily.daily))
    app_bot.add_handler(CommandHandler("pay", economy.give))
    app_bot.add_handler(CommandHandler("shop", shop.shop_menu))
    app_bot.add_handler(CommandHandler("buy", shop.buy))

    # ========= 3. RPG & BATTLE SYSTEM =========
    app_bot.add_handler(CommandHandler("battle", battle.battle_system))
    app_bot.add_handler(CommandHandler("battlelb", battle.battle_leaderboard))
    app_bot.add_handler(CommandHandler("arena", mafia.arena_fight))
    app_bot.add_handler(CommandHandler("kill", game.kill))
    app_bot.add_handler(CommandHandler("rob", game.rob))
    app_bot.add_handler(CommandHandler("protect", game.protect))

    # ========= 4. MAFIA TEAM SYSTEM (Withdraw/Bank Logs) =========
    app_bot.add_handler(CommandHandler("create_team", mafia.create_team))
    app_bot.add_handler(CommandHandler("join_team", mafia.join_team))
    app_bot.add_handler(CommandHandler("mpromote", mafia.promote_member))
    app_bot.add_handler(CommandHandler("team_war", mafia.team_war))
    app_bot.add_handler(CommandHandler("mafialb", mafia.team_leaderboard)) 
    app_bot.add_handler(CommandHandler("t_deposit", mafia.team_deposit))
    app_bot.add_handler(CommandHandler("t_withdraw", mafia.team_withdraw))
    app_bot.add_handler(CommandHandler("kick", mafia.kick_member))
    app_bot.add_handler(CommandHandler("leave", mafia.leave_team))

    # ========= 5. SOCIAL & FUN =========
    app_bot.add_handler(CommandHandler("marry", social.propose))
    app_bot.add_handler(CommandHandler("couple", couple.couple_roll))
    app_bot.add_handler(CommandHandler("love", love.love_command)) 
    app_bot.add_handler(CommandHandler("propose", social.propose))
    app_bot.add_handler(CommandHandler("divorce", social.divorce))
    app_bot.add_handler(CommandHandler("truth", fun.truth))
    app_bot.add_handler(CommandHandler("dare", fun.dare))
    app_bot.add_handler(CommandHandler("quiz", fun.quiz))

    # ========= 6. AI & CHATBOT (Unlimited Fast Reply) =========
    # Fixed: Toggle aur Ask commands sahi se link hain
    app_bot.add_handler(CommandHandler("chatbot", chatbot.chatbot_toggle)) 
    app_bot.add_handler(CommandHandler("ask", chatbot.ask_ai))
    app_bot.add_handler(CommandHandler("speak", ai_media.speak_command))
    app_bot.add_handler(CommandHandler("draw", ai_media.draw_command))

    # ========= 7. SYSTEM EVENTS & LOGGER (Group Add/Leave) =========
    app_bot.add_handler(CommandHandler("welcome", welcome.welcome_command))
    # Logger: Jab bot group join ya leave karega
    app_bot.add_handler(ChatMemberHandler(events.chat_member_update))
    app_bot.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome.new_member))

    # ========= 8. GAMES & CALLBACKS =========
    app_bot.add_handler(CommandHandler("word", wordseek.start_game))
    app_bot.add_handler(CommandHandler("riddle", riddle.riddle_command))
    app_bot.add_handler(CommandHandler("dice", fun.dice)) 
    app_bot.add_handler(CallbackQueryHandler(start.help_callback, pattern="^(start_|help_|return_|cb_|help_menu)"))
    app_bot.add_handler(CallbackQueryHandler(shop.shop_callback, pattern="^shop_"))
    app_bot.add_handler(CallbackQueryHandler(social.proposal_callback, pattern="^marry_"))

    # ========= 9. MESSAGE LISTENERS =========
    app_bot.add_handler(MessageHandler(filters.ChatType.GROUPS, events.group_tracker), group=1)
    
    # Chatbot Auto-Reply: Private aur Groups dono ke liye
    app_bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chatbot.ai_message_handler), group=6)
    
    app_bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, riddle.check_riddle_answer), group=4)
    app_bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, wishes.wishes_handler), group=5)

    # Final Launch
    print(f"✅ {BOT_NAME} DEPLOYED WITH FULL LOGGER & CHATBOT!")
    app_bot.run_polling(allowed_updates=Update.ALL_TYPES, drop_pending_updates=True)
