# app/subscriptions.py
from datetime import datetime, timedelta
from app.database import add_transaction, update_user_balance
from app.config import SUBSCRIPTION_PLANS, WALLET_ADDRESS
from app.admin import send_admin_notification


def handle_subscription(user_id, plan_key):
    """معالجة طلب الاشتراك"""
    if plan_key not in SUBSCRIPTION_PLANS:
        return None

    plan = SUBSCRIPTION_PLANS[plan_key]
    price = plan["price"]
    duration = plan["duration_days"]

    # إضافة معاملة جديدة
    add_transaction(user_id, "subscription", price, "pending")

    # إشعار الأدمن
    send_admin_notification(
        f"🔔 مستخدم {user_id} طلب الاشتراك في باقة {plan_key}\n"
        f"المبلغ المطلوب: {price} USDT"
    )

    return plan


def confirm_payment(user_id, plan_key):
    """تأكيد الدفع وتفعيل الاشتراك"""
    if plan_key not in SUBSCRIPTION_PLANS:
        return False

    plan = SUBSCRIPTION_PLANS[plan_key]
    price = plan["price"]
    duration = plan["duration_days"]

    # تحديث الرصيد
    update_user_balance(user_id, -price)

    # إشعار الأدمن
    send_admin_notification(
        f"✅ تم تأكيد اشتراك المستخدم {user_id} في {plan_key} لمدة {duration} يوم"
    )

    return True


def show_subscription_plans():
    """إرجاع قائمة الباقات"""
    text = "📌 خطط الاشتراك المتاحة:\n\n"
    for key, data in SUBSCRIPTION_PLANS.items():
        text += f"• {key.capitalize()} → {data['price']} USDT / {data['duration_days']} يوم\n"
    text += f"\n💳 ادفع على المحفظة التالية: \n`{WALLET_ADDRESS}`"
    return text


def show_withdraw_menu():
    """إظهار رسالة السحب"""
    return "💰 لطلب سحب الرصيد، الرجاء إرسال عنوان محفظتك والمبلغ المطلوب."
