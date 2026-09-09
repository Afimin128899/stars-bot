"""
Stars Bot - Main file
"""

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from telegram.constants import ParseMode
import uuid
import random

from config import BOT_TOKEN, ADMIN_ID, TASK_REWARD, MIN_WITHDRAWAL, STARS_RATE
from database import Database
from handlers import (
    cmd_start,
    cmd_profile,
    cmd_earn,
    cmd_bonus,
    cmd_tasks,
    cmd_withdraw,
    cmd_top,
    cmd_games,
    cmd_random,
    cmd_donate,
    button_callback,
    task_answer
)

# Logging setup
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Initialize database
db = Database()

async def main():
    """Start the bot"""
    # Create the Application
    application = Application.builder().token(BOT_TOKEN).build()

    # Register command handlers
    application.add_handler(CommandHandler("start", cmd_start))
    application.add_handler(CommandHandler("profile", cmd_profile))
    application.add_handler(CommandHandler("earn", cmd_earn))
    application.add_handler(CommandHandler("bonus", cmd_bonus))
    application.add_handler(CommandHandler("tasks", cmd_tasks))
    application.add_handler(CommandHandler("withdraw", cmd_withdraw))
    application.add_handler(CommandHandler("top", cmd_top))
    application.add_handler(CommandHandler("games", cmd_games))
    application.add_handler(CommandHandler("random", cmd_random))
    application.add_handler(CommandHandler("donate", cmd_donate))

    # Register callback handlers
    application.add_handler(CallbackQueryHandler(button_callback))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, task_answer))

    # Start the Bot
    await application.run_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
