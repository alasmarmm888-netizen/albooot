# app/config.py
import os
from dotenv import load_dotenv

# تحميل متغيرات البيئة من ملف .env
load_dotenv()

# توكنات البوتات
BOT_TOKEN = os.getenv("BOT_TOKEN")              # البوت الرئيسي
ADMIN_BOT_TOKEN = os.getenv("ADMIN_BOT_TOKEN")  # بوت الإدارة

# معرف الأدمن
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

# قنوات
ARCHIVE_CHANNEL_ID = int(os.getenv("ARCHIVE_CHANNEL_ID", "0"))
ERROR_CHANNEL_ID = int(os.getenv("ERROR_CHANNEL_ID", "0"))

# المحفظة
WALLET_ADDRESS = os.getenv("WALLET_ADDRESS", "USDT-ADDRESS-HERE")

# خطط الاشتراك
SUBSCRIPTION_PLANS = {
    "basic": {"price": 10, "duration_days": 30},
    "pro": {"price": 25, "duration_days": 90},
    "vip": {"price": 50, "duration_days": 180},
}
