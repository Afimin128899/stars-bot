"""
Configuration file for Stars Bot
"""

# Telegram Bot Token
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"

# Admin ID (для проверки выводов)
ADMIN_ID = 123456789

# Курс обмена
STARS_RATE = 1  # 1 звезда = 1 звезда (базовая)
GRAM_RATE = 1  # 1 звезда = 0.14 GRAM (примерно)
SEND_RATE = 1  # 1 звезда = 0.14 TON (Send)
XROCKET_RATE = 1  # 1 звезда = 0.14 USDT (xRocket)

# Курсы в GRAM, Send, xRocket (в долларах за 1 звезду)
GRAM_USD_RATE = 0.14  # 1 звезда = 0.14 GRAM
SEND_USD_RATE = 0.14  # 1 звезда = 0.14 TON
XROCKET_USD_RATE = 0.14  # 1 звезда = 0.14 USDT

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

# Платёжные системы
WITHDRAW_METHODS = {
    'telegram_stars': {'name': 'Telegram Stars', 'rate': STARS_RATE},
    'gram': {'name': 'GRAM', 'rate': GRAM_USD_RATE},
    'send': {'name': 'Send (@send)', 'rate': SEND_USD_RATE},
    'xrocket': {'name': 'xRocket (@xrocket)', 'rate': XROCKET_USD_RATE},
}
