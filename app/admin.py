# app/admin.py
from telegram import Bot
from app.config import BOT_TOKEN, ADMIN_ID

# بوت للتواصل المباشر مع الأدمن
bot = Bot(token=BOT_TOKEN)


def send_admin_notification(message: str):
    """إرسال إشعار إلى الأدمن"""
    try:
        if ADMIN_ID != 0:
            bot.send_message(chat_id=ADMIN_ID, text=message)
    except Exception as e:
        print(f"❌ فشل إرسال رسالة إلى الأدمن: {e}")
