# app/handlers.py
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from app.subscriptions import (
    handle_subscription,
    confirm_payment,
    show_subscription_plans,
    show_withdraw_menu,
)


# أمر /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📌 الاشتراك", callback_data="subscription_menu")],
        [InlineKeyboardButton("💰 السحب", callback_data="withdraw_menu")],
    ]
    await update.message.reply_text(
        "👋 أهلاً بك في البوت!\nاختر من القائمة:",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


# قائمة الاشتراكات
async def subscription_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    text = show_subscription_plans()
    keyboard = [
        [InlineKeyboardButton("Basic", callback_data="sub_basic")],
        [InlineKeyboardButton("Pro", callback_data="sub_pro")],
        [InlineKeyboardButton("VIP", callback_data="sub_vip")],
    ]
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))


# التعامل مع الاشتراك
async def handle_sub_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    plan_key = query.data.split("_")[1]  # sub_basic → basic
    plan = handle_subscription(query.from_user.id, plan_key)

    if plan:
        await query.edit_message_text(
            f"📌 اخترت باقة {plan_key.capitalize()}.\n"
            f"الرجاء الدفع: {plan['price']} USDT\n"
            f"إلى المحفظة: `{context.bot_data.get('wallet', 'غير محددة')}`"
        )
    else:
        await query.edit_message_text("❌ الباقة غير صحيحة.")


# قائمة السحب
async def withdraw_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    text = show_withdraw_menu()
    await query.edit_message_text(text)
