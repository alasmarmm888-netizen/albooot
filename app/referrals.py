import sqlite3
from datetime import date
from app.database import update_user_balance

DB_NAME = "trading_bot.db"

# ==================== إضافة عمولة الإحالة ====================
def add_referral_commission(referrer_id, referred_id, amount):
    """
    تحسب وتضيف عمولة 10% للمحيل
    """
    commission = amount * 0.10  # 10% عمولة
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # تحديث رصيد المحيل
    c.execute("UPDATE users SET balance = balance + ? WHERE user_id = ?", (commission, referrer_id))

    # تسجيل العملية
    c.execute('''INSERT INTO referrals (referrer_id, referred_id, commission_earned, referral_date)
                 VALUES (?, ?, ?, ?)''', (referrer_id, referred_id, commission, date.today()))

    conn.commit()
    conn.close()

    return commission

# ==================== جلب بيانات الإحالات ====================
def get_referral_stats(user_id):
    """
    ترجع عدد المدعوين وإجمالي العمولات للمستخدم
    """
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("SELECT COUNT(*) FROM referrals WHERE referrer_id = ?", (user_id,))
    referral_count = c.fetchone()[0]

    c.execute("SELECT SUM(commission_earned) FROM referrals WHERE referrer_id = ?", (user_id,))
    total_commissions = c.fetchone()[0] or 0

    conn.close()
    return referral_count, total_commissions
