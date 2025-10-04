import os
from telegram import Bot

ADMIN_BOT_TOKEN = os.getenv("8074752128:AAHkPJ1Acsk8i3l7X-IaeL2FhWGmYIbZzlg")
ARCHIVE_CHANNEL_ID = os.getenv("-1003178411340")
ERROR_CHANNEL_ID = os.getenv("-1003091305351")

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

