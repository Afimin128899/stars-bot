"""
Bot handlers for all commands and callbacks
"""

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
import uuid
import random
from database import Database
from config import ADMIN_ID, TASK_REWARD, MIN_WITHDRAWAL, STARS_RATE, REFERRAL_REWARDS, MIN_REFERRALS_FOR_REWARD

db = Database()

# Store active tasks
active_tasks = {}

async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start command - register user"""
    user = update.effective_user
    referrer_id = None
    
    # Check for referral link
    if context.args:
        try:
            referrer_id = int(context.args[0])
        except:
            pass
    
    # Create unique referral link
    referral_link = f"https://t.me/YourBotName?start={user.id}"
    
    # Add user to database
    db.add_user(
        user_id=user.id,
        username=user.username or "Unknown",
        first_name=user.first_name or "User",
        referral_link=referral_link,
        referrer_id=referrer_id
    )
    
    # Send welcome message with menu
    keyboard = [
        [InlineKeyboardButton("💰 Заработать", callback_data="earn")],
        [InlineKeyboardButton("🎁 Бонус", callback_data="bonus"), InlineKeyboardButton("🔥 Задания", callback_data="tasks")],
        [InlineKeyboardButton("⭐ Вывести", callback_data="withdraw"), InlineKeyboardButton("👤 Профиль", callback_data="profile")],
        [InlineKeyboardButton("🎮 Игры", callback_data="games"), InlineKeyboardButton("👑 Топ", callback_data="top")],
        [InlineKeyboardButton("🎲 Рандом", callback_data="random")],
        [InlineKeyboardButton("❤️ Донат", callback_data="donate")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        f"🌟 <b>Добро пожаловать в Stars Bot!</b>\n\n"
        f"Здесь ты можешь:\n"
        f"⭐ Зарабатывать звёзды\n"
        f"🎯 Выполнять задания\n"
        f"👥 Приглашать друзей\n"
        f"💸 Выводить свои звёзды\n\n"
        f"<i>Выбери раздел ниже 👇</i>",
        reply_markup=reply_markup,
        parse_mode=ParseMode.HTML
    )

async def cmd_profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show user profile"""
    user_id = update.effective_user.id
    stats = db.get_user_stats(user_id)
    
    message = (
        f"👤 <b>Ваш профиль</b>\n\n"
        f"⭐ Баланс: <b>{stats['stars']:.2f}</b>\n"
        f"👥 Рефералов: <b>{stats['referrals']}</b>\n"
        f"✅ Выполнено заданий: <b>{stats['completed_tasks']}</b>\n\n"
        f"🔗 Ваша реферальная ссылка:\n"
        f"<code>https://t.me/YourBotName?start={user_id}</code>"
    )
    
    keyboard = [
        [InlineKeyboardButton("← Назад в меню", callback_data="menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.callback_query:
        await update.callback_query.edit_message_text(
            message,
            parse_mode=ParseMode.HTML,
            reply_markup=reply_markup
        )
    else:
        await update.message.reply_text(
            message,
            parse_mode=ParseMode.HTML,
            reply_markup=reply_markup
        )

async def cmd_earn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Earn stars section"""
    message = (
        f"💰 <b>Способы заработка</b>\n\n"
        f"1️⃣ <b>Выполнение заданий</b> - Решай примеры, получай звёзды\n"
        f"2️⃣ <b>Реферальная программа</b> - Приглашай друзей за награды\n"
        f"3️⃣ <b>Бонусы</b> - Получай бонусы за определённые действия\n\n"
        f"Выбери способ:"
    )
    
    keyboard = [
        [InlineKeyboardButton("🔥 Задания", callback_data="tasks")],
        [InlineKeyboardButton("👥 Рефералы", callback_data="referrals")],
        [InlineKeyboardButton("🎁 Бонусы", callback_data="bonus")],
        [InlineKeyboardButton("← Назад в меню", callback_data="menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.callback_query:
        await update.callback_query.edit_message_text(
            message,
            parse_mode=ParseMode.HTML,
            reply_markup=reply_markup
        )
    else:
        await update.message.reply_text(
            message,
            parse_mode=ParseMode.HTML,
            reply_markup=reply_markup
        )

async def cmd_bonus(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Bonus section"""
    message = (
        f"🎁 <b>Бонусы</b>\n\n"
        f"✅ Ежедневный бонус - 5 ⭐\n"
        f"🌟 За подписку на канал - 10 ⭐\n"
        f"👑 Telegram Premium - +9 ⭐\n\n"
        f"Приходи завтра за новыми бонусами!"
    )
    
    keyboard = [
        [InlineKeyboardButton("← Назад в меню", callback_data="menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.callback_query:
        await update.callback_query.edit_message_text(
            message,
            parse_mode=ParseMode.HTML,
            reply_markup=reply_markup
        )
    else:
        await update.message.reply_text(
            message,
            parse_mode=ParseMode.HTML,
            reply_markup=reply_markup
        )

async def cmd_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Tasks section - math problems"""
    user_id = update.effective_user.id
    
    # Generate random math task
    num1 = random.randint(1, 100)
    num2 = random.randint(1, 100)
    operation = random.choice(["+", "-", "*"])
    
    if operation == "+":
        answer = num1 + num2
    elif operation == "-":
        answer = num1 - num2
    else:  # multiplication
        answer = num1 * num2
    
    # Create task in database
    task_id = db.create_task(user_id, num1, num2, operation, answer)
    
    # Store task info
    active_tasks[user_id] = {
        'task_id': task_id,
        'answer': answer
    }
    
    message = (
        f"🔥 <b>Решите пример для подтверждения:</b>\n\n"
        f"<code>{num1} {operation} {num2} = ?</code>\n\n"
        f"Ответ: <b>{TASK_REWARD} ⭐</b>\n\n"
        f"Напишите ответ в чат:"
    )
    
    keyboard = [
        [InlineKeyboardButton("← Назад в меню", callback_data="menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.callback_query:
        await update.callback_query.edit_message_text(
            message,
            parse_mode=ParseMode.HTML,
            reply_markup=reply_markup
        )
    else:
        await update.message.reply_text(
            message,
            parse_mode=ParseMode.HTML,
            reply_markup=reply_markup
        )

async def cmd_withdraw(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Withdraw stars section"""
    user_id = update.effective_user.id
    stars = db.get_stars(user_id)
    
    message = (
        f"⭐ <b>Вывести звёзды</b>\n\n"
        f"Ваш баланс: <b>{stars:.2f} ⭐</b>\n"
        f"Курс: 3 ⭐ = 1 Telegram Star\n\n"
        f"Минимум для вывода: <b>{MIN_WITHDRAWAL} ⭐</b>"
    )
    
    keyboard = []
    
    if stars >= MIN_WITHDRAWAL:
        withdraw_options = [15, 25, 50, 100]
        for amount in withdraw_options:
            if stars >= amount:
                stars_count = int(amount / STARS_RATE)
                keyboard.append([InlineKeyboardButton(
                    f"💰 {amount} ⭐ → {stars_count} Star",
                    callback_data=f"withdraw_{amount}"
                )])
    
    keyboard.append([InlineKeyboardButton("← Назад в меню", callback_data="menu")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.callback_query:
        await update.callback_query.edit_message_text(
            message,
            parse_mode=ParseMode.HTML,
            reply_markup=reply_markup
        )
    else:
        await update.message.reply_text(
            message,
            parse_mode=ParseMode.HTML,
            reply_markup=reply_markup
        )

async def cmd_top(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Top users leaderboard"""
    top_users = db.get_top_users(10)
    
    message = "👑 <b>Топ 10 пользователей</b>\n\n"
    for i, (user_id, name, stars) in enumerate(top_users, 1):
        medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
        message += f"{medal} <b>{name}</b> - {stars:.2f} ⭐\n"
    
    keyboard = [
        [InlineKeyboardButton("← Назад в меню", callback_data="menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.callback_query:
        await update.callback_query.edit_message_text(
            message,
            parse_mode=ParseMode.HTML,
            reply_markup=reply_markup
        )
    else:
        await update.message.reply_text(
            message,
            parse_mode=ParseMode.HTML,
            reply_markup=reply_markup
        )

async def cmd_games(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Games section"""
    message = (
        f"🎮 <b>Игры</b>\n\n"
        f"Скоро здесь появятся мини-игры для заработка!\n\n"
        f"🎲 Угадай число\n"
        f"🃏 Карточные игры\n"
        f"💣 Сапёр\n\n"
        f"Следи за обновлениями!"
    )
    
    keyboard = [
        [InlineKeyboardButton("← Назад в меню", callback_data="menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.callback_query:
        await update.callback_query.edit_message_text(
            message,
            parse_mode=ParseMode.HTML,
            reply_markup=reply_markup
        )
    else:
        await update.message.reply_text(
            message,
            parse_mode=ParseMode.HTML,
            reply_markup=reply_markup
        )

async def cmd_random(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Random rewards"""
    user_id = update.effective_user.id
    reward = random.randint(1, 10)
    db.add_stars(user_id, reward)
    
    message = (
        f"🎲 <b>Ты выиграл!</b>\n\n"
        f"+ {reward} ⭐\n\n"
        f"Приходи завтра за новой попыткой!"
    )
    
    keyboard = [
        [InlineKeyboardButton("← Назад в меню", callback_data="menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.callback_query:
        await update.callback_query.edit_message_text(
            message,
            parse_mode=ParseMode.HTML,
            reply_markup=reply_markup
        )
    else:
        await update.message.reply_text(
            message,
            parse_mode=ParseMode.HTML,
            reply_markup=reply_markup
        )

async def cmd_donate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Donate section"""
    message = (
        f"❤️ <b>Поддержи проект!</b>\n\n"
        f"Твоя поддержка помогает развивать бота и добавлять новые возможности!\n\n"
        f"Выбери сумму для пожертвования:"
    )
    
    keyboard = [
        [InlineKeyboardButton("⭐ 10 Stars", callback_data="donate_10")],
        [InlineKeyboardButton("⭐⭐ 50 Stars", callback_data="donate_50")],
        [InlineKeyboardButton("⭐⭐⭐ 100 Stars", callback_data="donate_100")],
        [InlineKeyboardButton("← Назад в меню", callback_data="menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.callback_query:
        await update.callback_query.edit_message_text(
            message,
            parse_mode=ParseMode.HTML,
            reply_markup=reply_markup
        )
    else:
        await update.message.reply_text(
            message,
            parse_mode=ParseMode.HTML,
            reply_markup=reply_markup
        )

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button callbacks"""
    query = update.callback_query
    await query.answer()
    
    data = query.data
    
    if data == "menu":
        keyboard = [
            [InlineKeyboardButton("💰 Заработать", callback_data="earn")],
            [InlineKeyboardButton("🎁 Бонус", callback_data="bonus"), InlineKeyboardButton("🔥 Задания", callback_data="tasks")],
            [InlineKeyboardButton("⭐ Вывести", callback_data="withdraw"), InlineKeyboardButton("👤 Профиль", callback_data="profile")],
            [InlineKeyboardButton("🎮 Игры", callback_data="games"), InlineKeyboardButton("👑 Топ", callback_data="top")],
            [InlineKeyboardButton("🎲 Рандом", callback_data="random")],
            [InlineKeyboardButton("❤️ Донат", callback_data="donate")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            "🌟 <b>Главное меню</b>",
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML
        )
    elif data == "earn":
        await cmd_earn(update, context)
    elif data == "bonus":
        await cmd_bonus(update, context)
    elif data == "tasks":
        await cmd_tasks(update, context)
    elif data == "withdraw":
        await cmd_withdraw(update, context)
    elif data == "profile":
        await cmd_profile(update, context)
    elif data == "top":
        await cmd_top(update, context)
    elif data == "games":
        await cmd_games(update, context)
    elif data == "random":
        await cmd_random(update, context)
    elif data == "donate":
        await cmd_donate(update, context)
    elif data.startswith("withdraw_"):
        amount = int(data.split("_")[1])
        user_id = update.effective_user.id
        stars = db.get_stars(user_id)
        
        if stars >= amount:
            db.remove_stars(user_id, amount)
            telegram_stars = int(amount / STARS_RATE)
            withdrawal_id = db.create_withdrawal(user_id, amount, telegram_stars)
            
            message = (
                f"✅ <b>Заявка на вывод создана!</b>\n\n"
                f"ID: #{withdrawal_id}\n"
                f"Сумма: {amount} ⭐ → {telegram_stars} Telegram Stars\n\n"
                f"Ожидайте рассмотрения администратором.\n"
                f"Обычно это занимает 5-30 минут."
            )
            
            keyboard = [
                [InlineKeyboardButton("← Назад в меню", callback_data="menu")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(
                message,
                parse_mode=ParseMode.HTML,
                reply_markup=reply_markup
            )

async def task_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle task answers"""
    user_id = update.effective_user.id
    
    if user_id not in active_tasks:
        return
    
    try:
        user_answer = int(update.message.text)
        task_info = active_tasks[user_id]
        
        is_correct = db.submit_task_answer(task_info['task_id'], user_answer)
        
        if is_correct:
            db.add_stars(user_id, TASK_REWARD)
            await update.message.reply_text(
                f"✅ <b>Правильно!</b>\n\n"
                f"+ {TASK_REWARD} ⭐\n\n"
                f"Твой баланс: {db.get_stars(user_id):.2f} ⭐",
                parse_mode=ParseMode.HTML
            )
        else:
            await update.message.reply_text(
                f"❌ <b>Неправильно!</b>\n\n"
                f"Правильный ответ: {task_info['answer']}\n\n"
                f"Попробуй ещё раз: /tasks",
                parse_mode=ParseMode.HTML
            )
        
        del active_tasks[user_id]
    except ValueError:
        await update.message.reply_text(
            "❌ Пожалуйста, введи число!",
            parse_mode=ParseMode.HTML
        )
