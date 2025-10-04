import sqlite3
from datetime import date, datetime

DB_NAME = "trading_bot.db"

# ==================== تهيئة قاعدة البيانات ====================
def init_database():
    """تهيئة قاعدة البيانات وإنشاء الجداول إذا لم تكن موجودة"""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # جدول المستخدمين
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        full_name TEXT,
        phone TEXT,
        country TEXT,
        balance REAL DEFAULT 0,
        referral_code TEXT,
        referred_by INTEGER,
        subscription_level TEXT,
        subscription_date DATE,
        registration_date DATE
    )''')

    # جدول العمليات
    c.execute('''CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        type TEXT,
        amount REAL,
        status TEXT,
        transaction_date DATETIME
    )''')

    # جدول الإحالات
    c.execute('''CREATE TABLE IF NOT EXISTS referrals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        referrer_id INTEGER,
        referred_id INTEGER,
        commission_earned REAL DEFAULT 0,
        referral_date DATE
    )''')

    conn.commit()
    conn.close()

# ==================== دوال المستخدمين ====================
def get_user_data(user_id):
    """جلب بيانات المستخدم"""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    user = c.fetchone()
    conn.close()
    return user

def register_user(user_id, full_name, phone, country, referral_code=None):
    """تسجيل مستخدم جديد"""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # إنشاء كود إحالة فريد
    user_referral_code = f"REF{user_id}{datetime.now().strftime('%H%M')}"

    # البحث عن المحيل إذا كان هناك كود إحالة
    referred_by = None
    if referral_code:
        c.execute("SELECT user_id FROM users WHERE referral_code = ?", (referral_code,))
        referrer = c.fetchone()
        if referrer:
            referred_by = referrer[0]

    c.execute('''INSERT OR REPLACE INTO users 
                 (user_id, full_name, phone, country, referral_code, referred_by, registration_date)
                 VALUES (?, ?, ?, ?, ?, ?, ?)''',
              (user_id, full_name, phone, country, user_referral_code, referred_by, date.today()))

    conn.commit()
    conn.close()

    return user_referral_code

def update_user_balance(user_id, amount):
    """تحديث رصيد المستخدم"""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE users SET balance = balance + ? WHERE user_id = ?", (amount, user_id))
    conn.commit()
    conn.close()

def add_transaction(user_id, transaction_type, amount, status="pending"):
    """إضافة معاملة جديدة"""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''INSERT INTO transactions (user_id, type, amount, status, transaction_date)
                 VALUES (?, ?, ?, ?, ?)''',
              (user_id, transaction_type, amount, status, datetime.now()))
    conn.commit()
    conn.close()
