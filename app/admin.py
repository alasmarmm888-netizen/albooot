from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
import sqlite3
from datetime import datetime, date
from app.database import get_user_data, update_user_balance, add_transaction
from app.subscriptions import SUBSCRIPTION_PLANS, WALLET_ADDRESS
from app.handlers import send_error_notification

# ==================== بدء لوحة الأدمن ====================
async def admin_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    # تحقق من صلاحية الأدمن
    if str(user_id) not in ["100317841", "763916290"]:  # ضع أيديك هنا
        await update.message.reply_text("❌ غير مصرح لك بالوصول!")
        return

    keyboard = [
        [InlineKeyboardButton("📊 الإحصائيات", callback_data="admin_stats")],
        [InlineKeyboardButton("👥 إدارة المستخدمين", callback_data="admin_users")],
        [InlineKeyboardButton("💳 طلبات السحب", callback_data="admin_withdrawals")],
        [InlineKeyboardButton("🔔 الإشعارات", callback_data="admin_notifications")],
        [InlineKeyboardButton("⚙️ إدارة المحافظ", callback_data="admin_wallets")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "🛠️ لوحة تحكم الأدمن\n\nاختر الإدارة المطلوبة:",
        reply_markup=reply_markup
    )

# ==================== إحصائيات النظام ====================
async def admin_stats(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    conn = sqlite3.connect("trading_bot.db")
    c = conn.cursor()

    c.execute("SELECT COUNT(*) FROM users")
    total_users = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM users WHERE subscription_level IS NOT NULL")
    subscribed_users = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM users WHERE registration_date = ?", (date.today(),))
    new_today = c.fetchone()[0]

    c.execute("SELECT SUM(balance) FROM users")
    total_balance = c.fetchone()[0] or 0

    c.execute("SELECT SUM(amount) FROM transactions WHERE type='deposit' AND status='completed'")
    total_deposits = c.fetchone()[0] or 0

    c.execute("SELECT SUM(amount) FROM transactions WHERE type='withdrawal' AND status='completed'")
    total_withdrawals = c.fetchone()[0] or 0

    c.execute("SELECT COUNT(*) FROM referrals")
    total_referrals = c.fetchone()[0]

    c.execute("SELECT SUM(commission_earned) FROM referrals")
    total_commissions = c.fetchone()[0] or 0

    conn.close()

    stats_text = (
        f"📊 إحصائيات النظام - {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
        f"👥 المستخدمين:\n• الإجمالي: {total_users}\n• المشتركين: {subscribed_users}\n• جدد اليوم: {new_today}\n\n"
        f"💰 المالية:\n• إجمالي الرصيد: {total_balance:.2f} USDT\n• إجمالي الإيداعات: {total_deposits:.2f} USDT\n• إجمالي السحبات: {total_withdrawals:.2f} USDT\n\n"
        f"🎁 الإحالات:\n• إجمالي الإحالات: {total_referrals}\n• إجمالي العمولات: {total_commissions:.2f} USDT\n\n🟢 النظام يعمل بشكل طبيعي"
    )

    keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="back_to_admin")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(stats_text, reply_markup=reply_markup)

# ==================== إدارة المستخدمين ====================
async def admin_users(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    conn = sqlite3.connect("trading_bot.db")
    c = conn.cursor()
    c.execute("SELECT user_id, full_name, balance, subscription_level FROM users ORDER BY registration_date DESC LIMIT 10")
    recent_users = c.fetchall()
    conn.close()

    users_text = "👥 آخر 10 مستخدمين:\n\n"
    for user in recent_users:
        user_id, full_name, balance, subscription = user
        sub_text = subscription if subscription else "غير مشترك"
        users_text += f"👤 {full_name}\n🆔 {user_id}\n💼 {balance:.2f} USDT\n📋 {sub_text}\n\n"

    keyboard = [
        [InlineKeyboardButton("🔍 بحث عن مستخدم", callback_data="admin_search_user")],
        [InlineKeyboardButton("📧 رسالة جماعية", callback_data="admin_broadcast")],
        [InlineKeyboardButton("🔙 رجوع", callback_data="back_to_admin")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(users_text, reply_markup=reply_markup)

# ==================== تأكيد الاشتراكات من الأدمن ====================
async def approve_subscription(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    data = query.data.split("_")
    user_id = int(data[2])
    plan_id = data[3]
    plan = SUBSCRIPTION_PLANS[plan_id]

    conn = sqlite3.connect("trading_bot.db")
    c = conn.cursor()
    c.execute("UPDATE users SET subscription_level=?, balance=balance+? WHERE user_id=?",
              (plan_id, plan['price'], user_id))
    c.execute("INSERT INTO transactions (user_id, type, amount, status, transaction_date) VALUES (?, ?, ?, ?, ?)",
              (user_id, "deposit", plan['price'], "completed", datetime.now()))
    conn.commit()
    conn.close()

    await query.answer("✅ تم تفعيل الاشتراك!")
    await query.edit_message_text(f"✅ تم تفعيل اشتراك المستخدم {user_id} بالخطة {plan['name']}")

    try:
        from telegram.ext import Application
        main_app = Application.builder().token("ضع_توكن_البوت_الرئيسي_هنا").build()
        await main_app.bot.send_message(
            chat_id=user_id,
            text=f"🎉 تم تأكيد اشتراكك بنجاح!\n📋 الخطة: {plan['name']}\n💰 الرصيد المضاف: {plan['price']} USDT\n⏳ المدة: {plan['days']} يوم"
        )
    except Exception as e:
        await send_error_notification(f"خطأ في إرسال إشعار للمستخدم {user_id}: {e}")
