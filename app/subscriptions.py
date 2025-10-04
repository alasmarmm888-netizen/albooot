# app/subscriptions.py
from datetime import datetime, timedelta
from telegram import Update
from telegram.ext import CallbackContext
from app.config import SUBSCRIPTION_PLANS, WALLET_ADDRESS
from app.database import add_subscription, get_user_data, update_subscription_status
from app.admin import send_admin_notification

# ============= بدء الاشتراك =============
def start_subscription(user_id: int, plan: str):
    """
    بدء عملية الاشتراك - يسجل بيانات الاشتراك ويطلب الدفع
    """
    if plan not in SUBSCRIPTION_PLANS:
        return False

    plan_data = SUBSCRIPTION_PLANS[plan]
    amount = plan_data["price"]
    duration_days = plan_data["duration_days"]

    # تسجيل الاشتراك كـ pending في قاعدة البيانات
    add_subscription(user_id, plan, amount, duration_days, status="pending")

    # إشعار الأدمن
    send_admin_notification(
        f"📢 مستخدم جديد بدأ عملية اشتراك:\n"
        f"🆔 ID: {user_id}\n"
        f"💳 الخطة: {plan.upper()}\n"
        f"💰 السعر: {amount} USDT\n"
        f"⌛ بانتظار الدفع..."
    )
    return True

# ============= تأكيد الدفع =============
def confirm_payment(user_id: int, tx_hash: str):
    """
    تأكيد الدفع يدويًا (بعد التحقق من المعاملة من قبل الأدمن)
    """
    user_data = get_user_data(user_id)
    if not user_data:
        return False

    # تحديث الاشتراك إلى active
    update_subscription_status(user_id, status="active")

    # إشعار الأدمن
    send_admin_notification(
        f"✅ تم تأكيد الدفع:\n"
        f"🆔 ID: {user_id}\n"
        f"📛 الاسم: {user_data.get('full_name', 'غير معروف')}\n"
        f"🔗 Tx: {tx_hash}"
    )
    return True

# ============= عرض الباقات =============
def show_subscription_plans(update: Update, context: CallbackContext):
    """
    إرسال قائمة الباقات المتاحة للمستخدم
    """
    text = "💳 خطط الاشتراك المتاحة:\n\n"
    for plan, details in SUBSCRIPTION_PLANS.items():
        text += f"🔹 {plan.upper()}: {details['price']} USDT ({details['duration_days']} يوم)\n"

    text += f"\n🚀 لإكمال الدفع، أرسل المبلغ إلى المحفظة التالية:\n`{WALLET_ADDRESS}`"

    update.message.reply_text(text, parse_mode="Markdown")

# ============= قائمة السحب (اختياري) =============
def show_withdraw_menu(update: Update, context: CallbackContext):
    """
    قائمة السحب (إذا فيه أرباح أو نظام ربح)
    """
    update.message.reply_text(
        "💸 للسحب، تواصل مع الدعم.\n"
        "📩 سيتم تحويل المبلغ بعد المراجعة."
    )
