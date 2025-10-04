# app/subscriptions.py
from datetime import datetime, timedelta
from app.config import SUBSCRIPTION_PLANS, WALLET_ADDRESS
from app.admin import send_admin_notification  # فقط دالة الإشعارات

# ====================== الاشتراكات ======================
user_subscriptions = {}  # لتخزين الاشتراكات مؤقتاً (يمكن ربطها بقاعدة البيانات لاحقاً)

def handle_subscription(user_id, plan_key):
    """
    معالجة الاشتراك: إضافة أو تجديد باقة
    """
    if plan_key not in SUBSCRIPTION_PLANS:
        return f"❌ الباقة {plan_key} غير موجودة."

    plan = SUBSCRIPTION_PLANS[plan_key]
    now = datetime.now()
    expiry_date = now + timedelta(days=plan["duration"])

    user_subscriptions[user_id] = {
        "plan": plan_key,
        "expiry": expiry_date
    }

    # إرسال إشعار للأدمن
    send_admin_notification(f"🎉 المستخدم {user_id} اشترك في باقة {plan['name']} بسعر {plan['price']}$")

    return f"✅ تم تفعيل باقة {plan['name']} حتى {expiry_date.strftime('%d/%m/%Y')}"

def show_subscription_plans():
    """
    عرض جميع الباقات المتاحة
    """
    message = "📦 باقات الاشتراك المتاحة:\n\n"
    for key, plan in SUBSCRIPTION_PLANS.items():
        message += f"{plan['name']} - {plan['price']}$ - لمدة {plan['duration']} يوم\n"
    return message

def confirm_payment(user_id, plan_key, amount_paid):
    """
    تأكيد الدفع والتحقق من صحة المبلغ
    """
    if plan_key not in SUBSCRIPTION_PLANS:
        return False, "الباقة غير موجودة."
    
    plan = SUBSCRIPTION_PLANS[plan_key]
    if amount_paid < plan["price"]:
        return False, f"المبلغ غير كافي. يجب دفع {plan['price']}$."
    
    # تفعيل الاشتراك
    handle_subscription(user_id, plan_key)
    return True, f"✅ تم تفعيل باقة {plan['name']} بنجاح."

def show_withdraw_menu(user_id):
    """
    مثال لإظهار قائمة السحب
    """
    return f"💰 محفظتك: {WALLET_ADDRESS}\nلا يمكن سحب أقل من 5$."
