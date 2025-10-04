from datetime import date, datetime
from app.database import update_user_balance, add_transaction
from app.admin import send_admin_notification  # استدعاء دالة الإشعارات من admin.py لتجنب circular import

# خطط الاشتراك
SUBSCRIPTION_PLANS = {
    "basic": 10,
    "premium": 25,
    "vip": 50
}

WALLET_ADDRESS = "WALLET_ADDRESS"  # ضع هنا رمز المحفظة إذا لم يكن في env

def handle_subscription(user_id, plan):
    if plan not in SUBSCRIPTION_PLANS:
        return False, "الخطة غير موجودة"
    
    amount = SUBSCRIPTION_PLANS[plan]
    update_user_balance(user_id, -amount)
    add_transaction(user_id, "subscription", amount, status="completed")

    # إشعار الإدارة
    send_admin_notification(f"المستخدم {user_id} اشترك في خطة {plan} مقابل {amount} دولار")
    return True, f"تم الاشتراك في خطة {plan} بنجاح"

def show_subscription_plans():
    return "\n".join([f"{plan}: ${price}" for plan, price in SUBSCRIPTION_PLANS.items()])

def confirm_payment(user_id, plan):
    # هنا يمكن إضافة منطق تأكيد الدفع إذا كان مرتبط بمنصة دفع
    pass

def show_withdraw_menu(user_id):
    # مثال لإظهار رصيد المستخدم مع خيار السحب
    return f"رصيدك الحالي: {get_user_balance(user_id)}\nاختر المبلغ للسحب."

