"""
Database module for Stars Bot
"""

import sqlite3
from datetime import datetime
from typing import Optional, List, Tuple

class Database:
    def __init__(self, db_name: str = "stars_bot.db"):
        self.db_name = db_name
        self.init_db()

    def init_db(self):
        """Initialize database tables"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        # Users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                stars REAL DEFAULT 0,
                referral_link TEXT UNIQUE,
                referrer_id INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_premium INTEGER DEFAULT 0
            )
        """)

        # Tasks table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                task_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                task_type TEXT,
                num1 INTEGER,
                num2 INTEGER,
                operation TEXT,
                correct_answer INTEGER,
                user_answer INTEGER,
                is_completed INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES users(user_id)
            )
        """)

        # Withdrawals table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS withdrawals (
                withdrawal_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                amount REAL,
                telegram_stars REAL,
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                completed_at TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES users(user_id)
            )
        """)

        # Referral rewards table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS referral_rewards (
                reward_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                referral_count INTEGER,
                reward_amount REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES users(user_id)
            )
        """)

        # Donations table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS donations (
                donation_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                amount REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES users(user_id)
            )
        """)

        conn.commit()
        conn.close()

    def add_user(self, user_id: int, username: str, first_name: str, referral_link: str, referrer_id: Optional[int] = None):
        """Add new user"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO users (user_id, username, first_name, referral_link, referrer_id)
                VALUES (?, ?, ?, ?, ?)
            """, (user_id, username, first_name, referral_link, referrer_id))
            conn.commit()
        except sqlite3.IntegrityError:
            pass
        finally:
            conn.close()

    def get_user(self, user_id: int) -> Optional[Tuple]:
        """Get user by ID"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        user = cursor.fetchone()
        conn.close()
        return user

    def add_stars(self, user_id: int, amount: float):
        """Add stars to user"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET stars = stars + ? WHERE user_id = ?", (amount, user_id))
        conn.commit()
        conn.close()

    def remove_stars(self, user_id: int, amount: float) -> bool:
        """Remove stars from user"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT stars FROM users WHERE user_id = ?", (user_id,))
        result = cursor.fetchone()
        
        if result and result[0] >= amount:
            cursor.execute("UPDATE users SET stars = stars - ? WHERE user_id = ?", (amount, user_id))
            conn.commit()
            conn.close()
            return True
        conn.close()
        return False

    def get_stars(self, user_id: int) -> float:
        """Get user stars"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT stars FROM users WHERE user_id = ?", (user_id,))
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else 0

    def create_withdrawal(self, user_id: int, amount: float, telegram_stars: float) -> int:
        """Create withdrawal request"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO withdrawals (user_id, amount, telegram_stars, status)
            VALUES (?, ?, ?, 'pending')
        """, (user_id, amount, telegram_stars))
        conn.commit()
        withdrawal_id = cursor.lastrowid
        conn.close()
        return withdrawal_id

    def get_pending_withdrawals(self) -> List[Tuple]:
        """Get all pending withdrawals"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM withdrawals WHERE status = 'pending'
            ORDER BY created_at ASC
        """)
        withdrawals = cursor.fetchall()
        conn.close()
        return withdrawals

    def approve_withdrawal(self, withdrawal_id: int):
        """Approve withdrawal"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE withdrawals SET status = 'approved', completed_at = CURRENT_TIMESTAMP
            WHERE withdrawal_id = ?
        """, (withdrawal_id,))
        conn.commit()
        conn.close()

    def reject_withdrawal(self, withdrawal_id: int):
        """Reject withdrawal and return stars"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT user_id, amount FROM withdrawals WHERE withdrawal_id = ?", (withdrawal_id,))
        result = cursor.fetchone()
        
        if result:
            user_id, amount = result
            cursor.execute("""
                UPDATE withdrawals SET status = 'rejected'
                WHERE withdrawal_id = ?
            """, (withdrawal_id,))
            cursor.execute("UPDATE users SET stars = stars + ? WHERE user_id = ?", (amount, user_id))
            conn.commit()
        conn.close()

    def get_referral_count(self, user_id: int) -> int:
        """Get count of referrals"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM users WHERE referrer_id = ?", (user_id,))
        count = cursor.fetchone()[0]
        conn.close()
        return count

    def get_top_users(self, limit: int = 10) -> List[Tuple]:
        """Get top users by stars"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT user_id, first_name, stars FROM users
            ORDER BY stars DESC
            LIMIT ?
        """, (limit,))
        users = cursor.fetchall()
        conn.close()
        return users

    def create_task(self, user_id: int, num1: int, num2: int, operation: str, answer: int) -> int:
        """Create new task"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO tasks (user_id, task_type, num1, num2, operation, correct_answer)
            VALUES (?, 'math', ?, ?, ?, ?)
        """, (user_id, num1, num2, operation, answer))
        conn.commit()
        task_id = cursor.lastrowid
        conn.close()
        return task_id

    def submit_task_answer(self, task_id: int, user_answer: int) -> bool:
        """Submit task answer"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE tasks SET user_answer = ?, is_completed = 1
            WHERE task_id = ?
        """, (user_answer, task_id))
        conn.commit()
        
        cursor.execute("SELECT correct_answer FROM tasks WHERE task_id = ?", (task_id,))
        result = cursor.fetchone()
        is_correct = result[0] == user_answer if result else False
        conn.close()
        return is_correct

    def add_donation(self, user_id: int, amount: float):
        """Add donation"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO donations (user_id, amount)
            VALUES (?, ?)
        """, (user_id, amount))
        conn.commit()
        conn.close()

    def get_user_stats(self, user_id: int) -> dict:
        """Get user statistics"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute("SELECT stars FROM users WHERE user_id = ?", (user_id,))
        stars = cursor.fetchone()[0] if cursor.fetchone() else 0
        
        cursor.execute("SELECT COUNT(*) FROM users WHERE referrer_id = ?", (user_id,))
        referrals = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM tasks WHERE user_id = ? AND is_completed = 1", (user_id,))
        completed_tasks = cursor.fetchone()[0]
        
        conn.close()
        return {
            'stars': stars,
            'referrals': referrals,
            'completed_tasks': completed_tasks
        }
