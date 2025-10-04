# app/config.py
import os
from dotenv import load_dotenv

# تحميل متغيرات البيئة من ملف .env
load_dotenv()

# ========== إعدادات البوت الرئيسي ==========
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("❌ BOT_TOKEN غير موجود في ملف .env")

# ========== إعدادات بوت الأدمن ==========
ADMIN_BOT_TOKEN = os.getenv("ADMIN_BOT_TOKEN")
if not ADMIN_BOT_TOKEN:
    raise ValueError("❌ ADMIN_BOT_TOKEN غير موجود في ملف .env")

ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID")
if not ADMIN_CHAT_ID:
    raise ValueError("❌ ADMIN_CHAT_ID غير موجود في ملف .env")

# ========== إعدادات القنوات ==========
ARCHIVE_CHANNEL_ID = os.getenv("ARCHIVE_CHANNEL_ID")  # قناة الأرشيف
ERROR_CHANNEL_ID = os.getenv("ERROR_CHANNEL_ID")      # قناة الأخطاء

if not ARCHIVE_CHANNEL_ID:
    raise ValueError("❌ ARCHIVE_CHANNEL_ID غير موجود في ملف .env")

if not ERROR_CHANNEL_ID:
    raise ValueError("❌ ERROR_CHANNEL_ID غير موجود في ملف .env")

# ========== إعدادات المحفظة ==========
WALLET_ADDRESS = os.getenv("WALLET_ADDRESS")
if not WALLET_ADDRESS:
    raise ValueError("❌ WALLET_ADDRESS غير موجود في ملف .env")

# ========== إعدادات الباقات ==========
# يمكن تعديل القيم في ملف .env أو هنا بشكل مباشر
SUBSCRIPTION_PLANS = {
    "basic": {
        "name": "الباقة الأساسية",
        "price": float(os.getenv("PLAN_BASIC_PRICE", "5.0")),  # دولار
        "duration": int(os.getenv("PLAN_BASIC_DAYS", "30"))    # أيام
    },
    "premium": {
        "name": "الباقة المميزة",
        "price": float(os.getenv("PLAN_PREMIUM_PRICE", "15.0")),
        "duration": int(os.getenv("PLAN_PREMIUM_DAYS", "90"))
    },
    "vip": {
        "name": "باقة VIP",
        "price": float(os.getenv("PLAN_VIP_PRICE", "40.0")),
        "duration": int(os.getenv("PLAN_VIP_DAYS", "365"))
    }
}
