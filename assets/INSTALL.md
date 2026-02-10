# 🛠️ دليل التثبيت (Installation Guide)

اتبع الخطوات التالية لتشغيل مشروع **Karioka Surveillance** على جهازك:

### 1. المتطلبات المسبقة
- تثبيت **Python 3.10** أو أحدث.
- في نظام Windows: يجب تثبيت أداة **Npcap** (ضرورية لعمل مكتبة Scapy في مسح ARP).
  - [تحميل Npcap من هنا](https://npcap.com/#download) (تأكد من تفعيل خيار *Install Npcap in WinPcap API-compatible Mode*).

### 2. إعداد البيئة الافتراضية
```powershell
# إنشاء البيئة
python -m venv venv

# تفعيل البيئة
.\venv\Scripts\activate
```

### 3. تثبيت المكتبات المطلوبة
```powershell
pip install -r requirements.txt
```

### 4. إعداد قاعدة البيانات
```powershell
python manage.py makemigrations
python manage.py migrate
```

### 5. تشغيل النظام
```powershell
python manage.py runserver
```
ثم افتح المتصفح على الرابط: `http://127.0.0.1:8000`
