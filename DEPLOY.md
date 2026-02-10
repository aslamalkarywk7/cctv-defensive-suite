# دليل رفع المشروع على PythonAnywhere 🚀

هذا الدليل يشرح كيفية رفع مشروع **Islam Al-Nashra Security Suite** على منصة PythonAnywhere.

## 1. المعلومات التقنية المستخدمة
*   **إصدار بايثون الموصى به**: `Python 3.10` أو `3.11`.
*   **إطار العمل**: `Django 5.2.x`.
*   **قاعدة البيانات**: `SQLite3` (مدمجة).

## 2. خطوات الرفع بالتفصيل

### الخطوة الأولى: رفع الكود
1. قم بضغط ملفات المشروع (Zip) ورفعها عبر تبويب **Files** في PythonAnywhere، أو استخدم `git clone` في الـ **Bash Console**.
2. افتح **Bash Console** وقم بفك الضغط إذا رفعت ملف Zip.

### الخطوة الثانية: إنشاء البيئة الافتراضية وتنصيب المكتبات
في الـ **Bash Console**، قم بتشغيل الأوامر التالية:
```bash
# إنشاء بيئة افتراضية
mkvirtualenv --python=/usr/bin/python3.10 myenv

# تنصيب المكتبات المطلوبة
pip install -r requirements.txt
```

### الخطوة الثالثة: إعداد قاعدة البيانات والملفات الثابتة
```bash
python manage.py migrate
python manage.py collectstatic
```

### الخطوة الرابعة: إعداد الـ Web App
1. اذهب إلى تبويب **Web** في PythonAnywhere.
2. اضغط **Add a new web app**.
3. اختر **Manual Configuration** (لا تختر Django لأننا قمنا بإعداده يدوياً).
4. اختر إصدار **Python 3.10**.
5. في إعدادات الـ Web App:
    *   **Source code**: ضع المسار الكامل لمجلد المشروع (مثلاً: `/home/yourusername/project_folder`).
    *   **Working directory**: نفس مسار الـ Source code.
    *   **Virtualenv**: ضع اسم البيئة التي أنشأتها (مثلاً: `myenv`).

### الخطوة الخامسة: إعداد ملف WSGI
في تبويب **Web**، اضغط على رابط **WSGI configuration file** وقم بمسح كل شيء وضع الكود التالي:
```python
import os
import sys

# مسار المشروع
path = '/home/yourusername/project_folder'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'core.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```
*(تأكد من تغيير `yourusername` و `project_folder` للمسارات الصحيحة).*

### الخطوة السادسة: إعداد الملفات الثابتة (Static Files)
في تبويب **Web**، انزل إلى قسم **Static files** وأضف:
*   **URL**: `/static/`
*   **Path**: المسار الكامل لمجلد `staticfiles` (الذي نتج عن أمر collectstatic).

## 3. ملاحظات هامة جداً ⚠️
1. **الرادار المحلي (Scanner)**: ميزة فحص الشبكة المحلية (ARP/Socket Radar) قد لا تعمل بكفاءة كاملة على السقيرفرات السحابية لأن البيئة تكون معزولة (Virtual Container)، لكن فحص الـ IPs الخارجية و الـ CVEs سيعمل بشكل ممتاز.
2. **DEBUG**: تم إغلاق وضع المطور (`DEBUG = False`) في الإعدادات لضمان الأمان عند الرفع.
3. **تحديث الكود**: في كل مرة تعدل فيها الكود، يجب الضغط على زر **Reload** في تبويب Web.

---
**بالتوفيق في الإطلاق!** 👨‍💻
