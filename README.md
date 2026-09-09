# Stars Bot 🌟

Telegram бот для заработка Telegram Stars через выполнение заданий, реферальную программу и бонусы.

## Функциональность

✅ **Система звёзд (RP★)**
- Заработок звёзд за решение примеров
- Реферальная программа с бонусами
- Система бонусов и подписок
- Вывод звёзд на Telegram Stars

✅ **Главное меню**
- 💰 Заработать - все способы заработка
- 🎁 Бонус - ежедневные бонусы
- 🔥 Задания - решение примеров
- ⭐ Вывести - конвертация RP→ Stars
- 👤 Профиль - статистика пользователя
- 🎮 Игры - минигры (в разработке)
- 👑 Топ - рейтинг пользователей
- 🎲 Рандом - случайные награды
- ❤️ Донат - поддержка проекта

## Установка

### 1. Клонирование репозитория
```bash
git clone https://github.com/Afimin128899/stars-bot.git
cd stars-bot
```

### 2. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 3. Конфигурация
Отредактируй `config.py`:
```python
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
ADMIN_ID = 123456789
```

Или создай `.env` файл на основе `.env.example`

### 4. Запуск бота
```bash
python main.py
```

## Получение Bot Token

1. Перейди в [@BotFather](https://t.me/botfather)
2. Отправь `/newbot`
3. Следуй инструкциям
4. Скопируй полученный token

## Структура проекта

```
stars-bot/
├── main.py           # Главный файл бота
├── handlers.py       # Обработчики команд
├── database.py       # Работа с БД
├── config.py         # Конфигурация
├── requirements.txt   # Зависимости
└── README.md         # Этот файл
```

## Конфигурация

### Награды за задания
```python
TASK_REWARD = 15  # RP★ за решение примера
```

### Реферальная система
```python
REFERRAL_REWARDS = {
    4: 6,      # 4-5 спонсоров = 6 RP★
    6: 9,      # 6-7 спонсоров = 9 RP★
    8: 12,     # 8-9 спонсоров = 12 RP★
    10: 15,    # 10+ спонсоров = 15 RP★
}
```

### Курс обмена
```python
STARS_RATE = 3  # 3 RP★ = 1 Telegram Star
```

## API используемых сервисов

- **Telegram Bot API** - управление ботом
- **SQLite** - хранение данных пользователей

## Разработка

### Добавление новых команд

1. Добавь обработчик в `handlers.py`
2. Зарегистрируй в `main.py`

```python
async def cmd_new_feature(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # твой код
    pass

# В main.py
application.add_handler(CommandHandler("newcommand", cmd_new_feature))
```

### Работа с БД

```python
from database import Database

db = Database()

# Добавить звёзды
db.add_stars(user_id, 10)

# Получить баланс
balance = db.get_stars(user_id)

# Получить статистику
stats = db.get_user_stats(user_id)
```

## Лицензия

MIT License

## Контакты

Главный разработчик: [@Afimin128899](https://t.me/Afimin128899)

## Поддержка

Если у тебя есть вопросы или предложения, создай Issue в репозитории!
