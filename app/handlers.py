import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from app.database import get_user_data, register_user, update_user_balance, add_transaction
from app.subscriptions import SUBSCRIPTION_PLANS, handle_subscription, confirm_payment, show_subscription_plans, show_withdraw_menu
from app.referrals import show_referral_system
from app.admin import admin_start, admin_stats, admin_users, approve_subscription, admin_wallets
from app.database import DB_NAME
import sqlite3
import logging

logger = logging.getLogger(__name__)

# ==================== إرسال إشعارات للأدمن ====================
async def send_admin_notification(message):
    """إرسال إشعار للأدمن"""
    try:
        # استدعاء بوت الأدمن هنا أو استخدم التوكن من env
        pass  # سيتم ملؤه لاحقاً في main.py
    except Exception as e:
        logger.error(f"خطأ في إرسال إشعار الأدمن: {e}")

async def send_error_notification(error_message):
    """إرسال إشعار خطأ"""
    try:
        pass  # سيتم ملؤه لاحقاً
    except Exception as e:
        logger.error(f"خطأ في إرسال إشعار الخطأ: {e}")

# ==================== معالجة تسجيل المستخدم ====================
async def handle_user_registration(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    user_input = update.message.text.strip()

    if 'awaiting_registration' in context.user_data:
        try:
            lines = user_input.split('\n')
            if len(lines) >= 3:
                full_name = lines[0].strip()
                phone = lines[1].strip()
                country = lines[2].strip()
                referral_code = lines[3].strip() if len(lines) > 3 and lines[3].strip().startswith('REF') else None

                user_referral_code = register_user(user_id, full_name, phone, country, referral_code)

                await update.message.reply_text(
                    f"🎉 تم تسجيلك بنجاح {full_name}!\n\n"
                    f"📋 بياناتك:\n"
                    f"👤 الاسم: {full_name}\n"
                    f"📞 الهاتف: {phone}\n"
                    f"🏳️ البلد: {country}\n"
                    f"🔗 كود دعوتك: {user_referral_code}\n\n"
                    f"🚀 الآن يمكنك اختيار خطة الاشتراك المناسبة لك!"
                )

                del context.user_data['awaiting_registration']

            else:
                await update.message.reply_text(
                    "❌ يرجى إدخال البيانات بالشكل الصحيح:\n"
                    "الاسم الثلاثي\nرقم الواتساب\nالبلد\n"
                    "مثال:\nمحمد أحمد علي\n966512345678\nالسعودية"
                )
        except Exception as e:
            await update.message.reply_text("❌ حدث خطأ في التسجيل، يرجى المحاولة مرة أخرى")
            await send_error_notification(f"خطأ في تسجيل المستخدم {user_id}: {e}")

# ==================== عرض القائمة الرئيسية ====================
async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    user_data = get_user_data(user_id)
    balance = user_data[4] if user_data else 0

    keyboard = [
        [InlineKeyboardButton("💼 خطط الاشتراك", callback_data="subscription_plans")],
        [InlineKeyboardButton("💰 رصيدي", callback_data="check_balance")],
        [InlineKeyboardButton("🎁 ادعو أصدقائك", callback_data="referral_system")],
        [InlineKeyboardButton("💳 سحب الأرباح", callback_data="withdraw_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        f"مرحباً بعودتك! 👋\n💼 محفظتك: {balance:.2f} USDT\n\nاختر من القائمة:",
        reply_markup=reply_markup
    )

# ==================== معالجة جميع الأزرار ====================
async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    data = query.data

    try:
        if data == "back_to_main":
            await show_main_menu(update, context)

        elif data == "back_to_admin":
            await admin_start(update, context)

        elif data == "subscription_plans":
            await show_subscription_plans(update, context)

        elif data.startswith("subscribe_"):
            await handle_subscription(update, context)

        elif data.startswith("confirm_payment_"):
            await confirm_payment(update, context)

        elif data == "referral_system":
            await show_referral_system(update, context)

        elif data == "withdraw_menu":
            await show_withdraw_menu(update, context)

        elif data == "admin_stats":
            await admin_stats(update, context)

        elif data == "admin_users":
            await admin_users(update, context)

        elif data == "admin_wallets":
            await admin_wallets(update, context)

        elif data.startswith("approve_sub_"):
            await approve_subscription(update, context)

        else:
            await query.answer("⚙️ هذه الخاصية قيد التطوير")

    except Exception as e:
        await query.answer("❌ حدث خطأ، يرجى المحاولة مرة أخرى")
        await send_error_notification(f"خطأ في معالجة الزر {data}: {e}")
