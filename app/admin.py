import os
from telegram import Bot

ADMIN_BOT_TOKEN = os.getenv("ADMIN_BOT_TOKEN")
ARCHIVE_CHANNEL_ID = os.getenv("ARCHIVE_CHANNEL_ID")
ERROR_CHANNEL_ID = os.getenv("ERROR_CHANNEL_ID")

admin_bot = Bot(token=ADMIN_BOT_TOKEN)

def send_admin_notification(message):
    if not ADMIN_BOT_TOKEN or not ARCHIVE_CHANNEL_ID:
        print("التحذير: لم يتم ضبط متغيرات البوت أو القناة في env")
        return
    try:
        admin_bot.send_message(chat_id=ARCHIVE_CHANNEL_ID, text=message)
    except Exception as e:
        print(f"خطأ عند إرسال إشعار للبوت الإداري: {e}")
        # محاولة إرسال رسالة الخطأ إلى قناة الأخطاء
        if ERROR_CHANNEL_ID:
            try:
                admin_bot.send_message(chat_id=ERROR_CHANNEL_ID, text=f"خطأ: {e}")
            except:
                pass
