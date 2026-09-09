"""
Configuration file for Stars Bot
"""

# Telegram Bot Token
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"

# Admin ID (для проверки выводов)
ADMIN_ID = 123456789

# Курсы обмена в USD (средние рыночные курсы)
GRAM_USD = 4.50  # 1 GRAM ≈ $4.50 USD
TON_USD = 7.20   # 1 TON ≈ $7.20 USD
USDT_USD = 1.00  # 1 USDT = $1.00 USD

# Курс обмена звезды
# 1 звезда = 0.01 GRAM
STARS_TO_GRAM = 0.01  # в GRAM
STARS_TO_TON = 0.01   # в TON (примерно)
STARS_TO_USDT = 0.072 # в USDT (0.01 GRAM * $4.50 = $0.045, 0.01 TON * $7.20 = $0.072)

# Награды за задания
TASK_REWARD = 0.3  # звезды за решение примера

# Реферальная система
REFERRAL_REWARDS = {
    4: 2,      # 4-5 спонсоров = 2 звезды
    6: 2.5,    # 6-7 спонсоров = 2.5 звезды
    8: 3,      # 8-9 спонсоров = 3 звезды
    10: 3.5,   # 10+ спонсоров = 3.5 звезды
}

# Минимум для вывода
MIN_WITHDRAWAL = 15

# Минимум рефералов для награды
MIN_REFERRALS_FOR_REWARD = 4

# Telegram Premium бонус
PREMIUM_BONUS = 0.5

# Database
DB_NAME = "stars_bot.db"

# Логирование
DEBUG = True

# Платежные системы
WITHDRAW_METHODS = {
    'gram': {'name': 'GRAM', 'rate': STARS_TO_GRAM, 'usd_rate': GRAM_USD},
    'send': {'name': 'Send (TON)', 'rate': STARS_TO_TON, 'usd_rate': TON_USD},
    'xrocket': {'name': 'xRocket (USDT)', 'rate': STARS_TO_USDT, 'usd_rate': USDT_USD},
}
