# app/main.py
import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# استيراد handlers من الملفات الأخرى
from handlers import start_handler, echo_handler
from subscriptions import subscribe_handler, unsubscribe_handler
from admin import admin_command_handler

# إعداد تسجيل الأخطاء
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# إنشاء التطبيق مع التوكن من environment
TOKEN = os.environ.get("7566859808:AAHI0WzczJ2nDmuzRI-F-WzxyUS9SglkvwE")
if not TOKEN:
    raise ValueError("BOT_TOKEN غير موجود في environment variables")

app = ApplicationBuilder().token(TOKEN).build()

# إضافة الـ handlers
app.add_handler(start_handler)
app.add_handler(echo_handler)
app.add_handler(subscribe_handler)
app.add_handler(unsubscribe_handler)
app.add_handler(admin_command_handler)

# Optional: handler لأي رسالة لم يتم التعرف عليها
async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("عذرًا، لا أفهم هذا الأمر.")

app.add_handler(MessageHandler(filters.COMMAND, unknown))

# تشغيل البوت
if name == "main":
    logging.info("البوت بدأ التشغيل...")
    app.run_polling()

