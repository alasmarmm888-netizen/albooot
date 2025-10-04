# app/handlers.py
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, CallbackQueryHandler
from app.config import SUBSCRIPTION_PLANS, ADMIN_ID
from app.database import register_user, get_user_data
from app.subscriptions import start_subscription
from app.admin import send_admin_notification

# ============= أوامر أساسية =============

def start(update: Update, context: CallbackContext):
    """أمر /start"""
    user = update.effective_user
    register_user(user.id, user.full_name, phone=None, country=None)

    update.message.reply_text(
        f"👋 أهلاً {user.full_name}!\n"
        "أنا بوت الاشتراكات.\n"
        "استخدم /subscribe لاختيار الباقة المناسبة."
    )

def help_command(update: Update, context: CallbackContext):
    """أمر /help"""
    update.message.reply_text(
        "📌 الأوامر المتاحة:\n"
        "/start - بدء الاستخدام\n"
        "/help - المساعدة\n"
        "/subscribe - عرض خطط الاشتراك"
    )

def subscribe_command(update: Update, context: CallbackContext):
    """أمر /subscribe - عرض خطط الاشتراك"""
    keyboard = [
        [InlineKeyboardButton(f"{plan.upper()} - {details['price']} USDT", callback_data=f"subscribe_{plan}")]
        for plan, details in SUBSCRIPTION_PLANS.items()
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("💳 اختر خطة الاشتراك:", reply_markup=reply_markup)

# ============= التعامل مع الأزرار =============

def button_callback(update: Update, context: CallbackContext):
    """التعامل مع ضغط الأزرار"""
    query = update.callback_query
    query.answer()

    if query.data.startswith("subscribe_"):
        plan = query.data.split("_")[1]
        user = query.from_user

        # بدء عملية الاشتراك
        start_subscription(user.id, plan)

        query.edit_message_text(
            text=f"✅ تم اختيار خطة *{plan.upper()}*.\n\n"
                 f"💰 السعر: {SUBSCRIPTION_PLANS[plan]['price']} USDT\n"
                 f"📅 المدة: {SUBSCRIPTION_PLANS[plan]['duration_days']} يوم\n\n"
                 f"🚀 أرسل المبلغ إلى المحفظة لإكمال الاشتراك."
        )

        # إشعار الأدمن
        send_admin_notification(
            f"👤 مستخدم جديد طلب اشتراك:\n"
            f"🆔 ID: {user.id}\n"
            f"📛 الاسم: {user.full_name}\n"
            f"💳 الخطة: {plan.upper()}"
        )

def handle_message(update: Update, context: CallbackContext):
    """أي رسالة نصية غير الأوامر"""
    update.message.reply_text("🤖 استخدم الأوامر المتاحة. اكتب /help للمساعدة.")

# ============= ربط الكولباك =============
def register_handlers(dp):
    dp.add_handler(CallbackQueryHandler(button_callback))
