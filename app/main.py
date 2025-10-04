# app/main.py
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import logging

# إعداد تسجيل الأخطاء
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# دالة /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("مرحبًا! أنا بوت تيليجرام الخاص بك.")

# دالة لمعالجة الرسائل النصية
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"لقد أرسلت: {update.message.text}")

# إنشاء التطبيق
app = ApplicationBuilder().token("7566859808:AAHI0WzczJ2nDmuzRI-F-WzxyUS9SglkvwE").build()

# إضافة الـ handlers
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), echo))

# تشغيل البوت
if __name__ == "__main__":
    app.run_polling()


