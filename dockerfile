# استخدام Python 3.11 كصورة أساسية
FROM python:3.11-slim

# تحديد مجلد العمل داخل الحاوية
WORKDIR /app

# نسخ ملف المتطلبات وتثبيتها
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# نسخ جميع ملفات المشروع
COPY . .

# أمر التشغيل عند بدء الحاوية
CMD ["python", "-m", "app/main.py"]

