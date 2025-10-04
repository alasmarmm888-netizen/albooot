# app/utils.py
from telegram import Bot
from app.main import ADMIN_BOT_TOKEN, ARCHIVE_CHANNEL_ID

async def send_admin_notification(message: str):
    """إرسال رسالة للإدارة"""
    try:
        bot = Bot(token=ADMIN_BOT_TOKEN)
        await bot.send_message(chat_id=ARCHIVE_CHANNEL_ID, text=message)
    except Exception as e:
        print(f"❌ خطأ في إرسال إشعار للأدمن: {e}")
