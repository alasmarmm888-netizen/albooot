from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from app.database import get_user_data, update_user_balance, add_transaction
from app.handlers import send_admin_notification
from datetime import datetime

# ==================== خطط الاشتراك ====================
SUBSCRIPTION_PLANS = {
    "bronze": {"name": "🟤 البرونزية", "price": 100, "days": 3, "profits": "10% - 20%"},
    "silver": {"name": "⚪ الفضية", "price": 500, "days": 3, "profits": "15% - 25%"},
    "gold": {"name": "🟡 الذهبية", "price": 1000, "days": 7, "profits": "20% - 35%"},
    "platinum": {"name": "🔵 البلاتينية", "price": 5000, "days": 15, "profits": "35% - 50%"},
    "diamond": {"name": "🔶 الماسية", "price": 10000, "days": 30, "profits": "50% - 80%"},
    "royal": {"name": "🟣 الملكية", "price": 20000, "days": 30, "profits": "حتى 100%"},
    "legendary": {"name": "🟠 الأسطورية", "price": 50000, "days": 30, "profits": "120% - 150%"}
}

WALLET_ADDRESS = "ضع_عنوان_المحفظة_هنا"

# ==================== عرض جميع خطط الاشتراك ====================
async def show_subscription_plans(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    keyboard = []
    for plan_id, plan in SUBSCRIPTION_PLANS.items():
        keyboard.append([InlineKeyboardButton(f"{plan['name']} - {plan['price']} USDT", callback_data=f"subscribe_{plan_id}")])

    keyboard.append([InlineKeyboardButton("🔙 رجوع", callback_data="back_to_main")])
    reply_markup = InlineKeyboardMarkup(keyboard)

    plans_text = "💼 خطط الاشتراك المتاحة:\n\n"
    for plan_id, plan in SUBSCRIPTION_PLANS.items():
        plans_text += f"{plan['name']}\n💰 السعر: {plan['price']} USDT\n⏳ المدة: {plan['days']} يوم\n📈 الأرباح: {plan['profits']}\n\n"

    await query.edit_message_text(plans_text, reply_markup=reply_markup)

# ==================== معالجة اختيار الاشتراك ====================
async def handle_subscription(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    plan_id = query.data.split("_")[1]
    plan = SUBSCRIPTION_PLANS[plan_id]
    await query.answer()

    subscription_text = (
        f"🎉 تم اختيار خطتك بنجاح!\n\n"
        f"🔹 الخطة: {plan['name']}\n"
        f"💰 السعر: {plan['price']} USDT\n"
        f"⏳ المدة: {plan['days']} يوم\n"
        f"📊 الأرباح المتوقعة: {plan['profits']}\n\n"
        f"💡 للمتابعة يرجى إتمام عملية الدفع على العنوان التالي:\n"
        f"`{WALLET_ADDRESS}`\n\n"
        f"⚠️ ملاحظة:\n"
        f"• التحويل فقط عبر شبكة TRC20\n"
        f"• سيتم تفعيل اشتراكك خلال 15 دقيقة بعد التأكيد\n\n"
        f"بعد الدفع، اضغط على زر تأكيد الدفع وأرسل صورة التحويل"
    )

    keyboard = [
        [InlineKeyboardButton("📸 تأكيد الدفع وإرسال الإثبات", callback_data=f"confirm_payment_{plan_id}")],
        [InlineKeyboardButton("🔙 رجوع للخطط", callback_data="subscription_plans")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(subscription_text, reply_markup=reply_markup, parse_mode='Markdown')

    # إشعار الأدمن
    user = get_user_data(query.from_user.id)
    user_name = user[1] if user else query.from_user.first_name
    await send_admin_notification(
        f"🔄 طلب اشتراك جديد\n👤 المستخدم: {user_name}\n🆔 {query.from_user.id}\n"
        f"📋 الخطة: {plan['name']}\n💰 المبلغ: {plan['price']} USDT"
    )

# ==================== تأكيد الدفع ====================
async def confirm_payment(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    plan_id = query.data.split("_")[2]
    plan = SUBSCRIPTION_PLANS[plan_id]
    await query.answer()

    await query.edit_message_text(
        f"📸 جاهز لاستلام إثبات الدفع للخطة {plan['name']}\n\n"
        f"💰 المبلغ: {plan['price']} USDT\n\n"
        f"يرجى إرسال صورة إشعار التحويل الآن\n"
        f"⚠️ تأكد من ظهور المبلغ، عنوان المحفظة، وتاريخ التحويل"
    )

    context.user_data['awaiting_payment_proof'] = plan_id
