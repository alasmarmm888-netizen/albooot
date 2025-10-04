# app/config.py
import os
from dotenv import load_dotenv

# تحميل المتغيرات من .env
load_dotenv()

# بيانات التوكنات
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))  # ID الأدمن (تضعه في ملف .env)

# عنوان المحفظة
WALLET_ADDRESS = os.getenv("WALLET_ADDRESS", "USDT-ADDRESS-HERE")

# خطط الاشتراك
SUBSCRIPTION_PLANS = {
    "basic": {"price": 10, "duration_days": 30},
    "pro": {"price": 25, "duration_days": 90},
    "vip": {"price": 50, "duration_days": 180},
}
