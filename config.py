"""
Configuration file for Stars Bot
"""

# Telegram Bot Token
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"

# Admin ID (для проверки выводов)
ADMIN_ID = 123456789

# Курс обмена
STARS_RATE = 3  # 3 ⭐ = 1 Telegram Star

# Награды за задания
TASK_REWARD = 15  # ⭐ за решение примера

# Реферальная система
REFERRAL_REWARDS = {
    4: 6,      # 4-5 спонсоров = 6 ⭐
    6: 9,      # 6-7 спонсоров = 9 ⭐
    8: 12,     # 8-9 спонсоров = 12 ⭐
    10: 15,    # 10+ спонсоров = 15 ⭐
}

# Минимум для вывода
MIN_WITHDRAWAL = 15

# Минимум рефералов для награды
MIN_REFERRALS_FOR_REWARD = 4

# Telegram Premium бонус
PREMIUM_BONUS = 9

# Database
DB_NAME = "stars_bot.db"

# Логирование
DEBUG = True
