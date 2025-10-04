import time
from threading import Thread
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters
from app.database import init_database
from app.handlers import (
    start, handle_user_registration, handle_payment_proof,
    handle_buttons
)
from app.admin import admin_start
import schedule

# ==================== إعداد التقارير التلقائية ====================
def setup_scheduled_reports():
    """إعداد التقارير التلقائية"""
    # يمكن ربطها مع وظائف send_daily_report / send_hourly_report
    # الآن مؤقتًا سنتركها فارغة لتجنب أخطاء الاستدعاء
    def run_scheduler():
        while True:
            schedule.run_pending()
            time.sleep(1)
    scheduler_thread = Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()

# ==================== التشغيل الرئيسي ====================
def main():
    print("🚀 بدء تشغيل البوت...")
    # تهيئة قاعدة البيانات
    init_database()
    print("✅ قاعدة البيانات مهيأة")

    # إعداد التقارير التلقائية
    setup_scheduled_reports()
    print("✅ التقارير التلقائية جاهزة")

    # إنشاء تطبيق البوت الرئيسي
    from app.database import DB_NAME
    from app.admin import approve_subscription
    from app.subscriptions import SUBSCRIPTION_PLANS, WALLET_ADDRESS

    MAIN_BOT_TOKEN = "ضع_توكن_البوت_الرئيسي_هنا"
    ADMIN_BOT_TOKEN = "ضع_توكن_بوت_الأدمن_هنا"

    main_app = Application.builder().token(MAIN_BOT_TOKEN).build()
    admin_app = Application.builder().token(ADMIN_BOT_TOKEN).build()

    # handlers للبوت الرئيسي
    main_app.add_handler(CommandHandler("start", start))
    main_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_user_registration))
    main_app.add_handler(MessageHandler(filters.PHOTO, handle_payment_proof))
    main_app.add_handler(CallbackQueryHandler(handle_buttons))

    # handlers بوت الإدارة
    admin_app.add_handler(CommandHandler("start", admin_start))
    admin_app.add_handler(CommandHandler("admin", admin_start))
    admin_app.add_handler(CallbackQueryHandler(handle_buttons))

    print("✅ البوت الرئيسي جاهز - التوكن:", MAIN_BOT_TOKEN[:10] + "...")
    print("✅ بوت الإدارة جاهز - التوكن:", ADMIN_BOT_TOKEN[:10] + "...")

    # تشغيل البوتات في threads منفصلة
    def run_main_bot():
        main_app.run_polling()

    def run_admin_bot():
        admin_app.run_polling()

    main_thread = Thread(target=run_main_bot, daemon=True)
    admin_thread = Thread(target=run_admin_bot, daemon=True)

    main_thread.start()
    admin_thread.start()

    print("🎉 جميع البوتات شغالة الآن!")

    # إبقاء البرنامج شغال
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("⏹️ إيقاف النظام...")

if __name__ == "__main__":
    main()
