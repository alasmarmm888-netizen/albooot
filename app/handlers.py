from app.database import get_user_data, register_user
from app.subscriptions import SUBSCRIPTION_PLANS, handle_subscription, show_subscription_plans, show_withdraw_menu
from app.admin import send_admin_notification  # استدعاء دالة الإشعارات مباشرة من admin.py

def start_command(user_id, full_name, phone, country, referral_code=None):
    user = get_user_data(user_id)
    if not user:
        code = register_user(user_id, full_name, phone, country, referral_code)
        send_admin_notification(f"تم تسجيل مستخدم جديد: {full_name}, معرف: {user_id}, كود الإحالة: {code}")
        return f"مرحباً {full_name}! تم تسجيلك بنجاح."
    else:
        return "أنت مسجل مسبقاً."

def subscription_command(user_id, plan):
    success, msg = handle_subscription(user_id, plan)
    return msg

def balance_command(user_id):
    user = get_user_data(user_id)
    if user:
        return f"رصيدك الحالي: {user[4]}$"
    return "المستخدم غير موجود."

def withdraw_command(user_id, amount):
    user = get_user_data(user_id)
    if not user:
        return "المستخدم غير موجود."
    if user[4] < amount:
        return "الرصيد غير كافي."
    # خصم الرصيد
    from app.database import update_user_balance, add_transaction
    update_user_balance(user_id, -amount)
    add_transaction(user_id, "withdraw", amount, status="pending")
    send_admin_notification(f"المستخدم {user_id} طلب سحب مبلغ {amount}$")
    return f"تم تقديم طلب السحب بمبلغ {amount}$ بنجاح."
