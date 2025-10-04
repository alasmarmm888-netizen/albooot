# app/admin.py
import os
import logging
from telegram import Bot
from app.config import ADMIN_BOT_TOKEN, ADMIN_CHAT_ID

# إعداد البوت الخاص بالإدارة
admin_bot = Bot(token=ADMIN_BOT_TOKEN)

# ============= إرسال إشعار للإدمن =============
def send_admin_notification(message: str):
    """
    إرسال رسالة إشعار إلى بوت الأدمن
    """
    try:
        admin_bot.send_message(
            chat_id=ADMIN_CHAT_ID,
            text=message,
            parse_mode="Markdown"
        )
        logging.info("تم إرسال إشعار إلى الأدمن بنجاح.")
    except Exception as e:
        logging.error(f"فشل إرسال إشعار إلى الأدمن: {e}")
