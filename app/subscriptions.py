import sqlite3
from datetime import datetime
from app.database import get_user_data, update_user_balance, add_transaction
from app.admin import send_admin_notification  # استدعاء دالة الإشعارات من admin.py لتجنب circular import

# مثال خطط الاشتراك
SUBSCRIPTION_PLANS = {
    "basic": {"name": "Basic", "price": 10, "days": 7},
    "premium": {"name": "Premium", "price": 30, "days": 30},
}

# ==================== معالجة الاشتراك ====================
async def handle_subscription(update, context):
    query = update.callback_query
    data = query.data.split("_")
    plan_id = data[1]
    user_id = query.from_user.id

    plan = SUBSCRIPTION_PLANS.get(plan_id)
    if not plan:
        await query.answer("❌ خطة غير موجودة")
        return

    # إضافة الرصيد للمستخدم
    update_user_balance(user_id, plan["price"])
    add_transaction(user_id, "deposit", plan["price"], "completed")

    await query.answer(f"✅ تم تفعيل اشتراكك بالخطة {plan['name']}")

    # إرسال إشعار للأدمن
    await send_admin_notification(f"مستخدم {user_id} اشترك في خطة {plan['name']}")

# ==================== تأكيد الدفع ====================
async def confirm_payment(update, context):
    query = update.callback_query
    await query.answer("✅ تم تأكيد الدفع")
    # يمكنك إضافة أي منطق إضافي لتأكيد الدفع

# ==================== عرض الخطط ====================
async def show_subscription_plans(update, context):
    from telegram import InlineKeyboardButton, InlineKeyboardMarkup

    keyboard = [
        [InlineKeyboardButton(f"{plan['name']} - {plan['price']}$", callback_data=f"subscribe_{plan_id}")]
        for plan_id, plan in SUBSCRIPTION_PLANS.items()
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("اختر خطة الاشتراك:", reply_markup=reply_markup)

# ==================== عرض قائمة السحب ====================
async def show_withdraw_menu(update, context):
    from telegram import InlineKeyboardButton, InlineKeyboardMarkup

    keyboard = [
        [InlineKeyboardButton("💵 سحب الأموال", callback_data="withdraw")],
        [InlineKeyboardButton("🔙 رجوع", callback_data="back_to_main")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("قائمة السحب:", reply_markup=reply_markup)
