from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CallbackQueryHandler, CommandHandler, MessageHandler, filters
from app.database import get_user_data
from app.subscriptions import (
    SUBSCRIPTION_PLANS,
    handle_subscription,
    confirm_payment,
    show_subscription_plans,
    show_withdraw_menu
)

# ==================== إرسال إشعارات للأدمن ====================
async def send_admin_notification(message: str):
    from app.main import ADMIN_CHAT_ID, main_app
    try:
        await main_app.bot.send_message(chat_id=ADMIN_CHAT_ID, text=message)
    except Exception as e:
        print(f"❌ خطأ في إرسال إشعار للأدمن: {e}")

# ==================== معالجة الأزرار العامة ====================
async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data

    try:
        if data.startswith("subscribe_"):
            await handle_subscription(update, context)
        elif data.startswith("confirm_payment_"):
            await confirm_payment(update, context)
        elif data == "subscription_plans":
            await show_subscription_plans(update, context)
        elif data == "withdraw_menu":
            await show_withdraw_menu(update, context)
        else:
            await query.answer("⚙️ هذه الخاصية قيد التطوير")
    except Exception as e:
        await query.answer("❌ حدث خطأ، يرجى المحاولة مرة أخرى")
        await send_admin_notification(f"خطأ في معالجة الزر {data}: {e}")
