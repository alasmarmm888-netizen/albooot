# app/main.py
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from app.handlers import (
    start,
    help_command,
    subscribe_command,
    handle_message,
)
from app.database import init_database
from app.config import BOT_TOKEN

# تهيئة قاعدة البيانات
init_database()

# إعداد تسجيل الأخطاء
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def main():
    """تشغيل البوت الرئيسي"""
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    # الأوامر الأساسية
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler("subscribe", subscribe_command))

    # استقبال أي رسالة نصية
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # تشغيل البوت
    updater.start_polling()
    logger.info("🚀 البوت يعمل الآن...")
    updater.idle()


if __name__ == "__main__":
    main()
