# 🛡️ Islam Al-Nashra Security Suite - CCTV & Camera Preview

**إسلام النشرة سكيورتي سويت** هو نظام متقدم مبني باستخدام Django لإدارة وفحص كاميرات المراقبة (CCTV) والشبكات المحلية. يهدف المشروع إلى توفير أدوات أمنية للمتخصصين لفحص الثغرات، استكشاف الشبكة، وعرض بث الكاميرات بطريقة منظمة.

---

## 🚀 الروابط السريعة
- [📄 دليل المساهمة (CONTRIBUTING.md)](CONTRIBUTING.md)
- [⚖️ رخصة المشروع (LICENSE)](LICENSE)
- [📂 هيكل المشروع التفصيلي (PROJECT_STRUCTURE.md)](PROJECT_STRUCTURE.md)
- [🛠️ دليل الرفع (DEPLOY.md)](DEPLOY.md)

---

## ✨ المميزات الرئيسية
- **رادار الشبكة (Network Scanner):** فحص الأجهزة المتصلة بالشبكة المحلية باستخدام ARP و Sockets.
- **إدارة الكاميرات (CCTV Manager):** إضافة، تعديل، وعرض الكاميرات مع دعم كلمات المرور الافتراضية.
- **فحص الثغرات (CVE Scanner):** البحث عن الثغرات المعروفة للأجهزة المكتشفة.
- **تقارير احترافية:** توليد تقارير بصيغة PDF لنتائج الفحص.
- **واجهة مستخدم عصرية:** متوافقة مع جميع الأجهزة (Responsive Design).

---

## 🛠️ التقنيات المستخدمة
- **Backend:** [Django 5.x](https://www.djangoproject.com/)
- **Image Processing:** [OpenCV](https://opencv.org/)
- **Networking:** [Scapy](https://scapy.net/), [Requests](https://requests.readthedocs.io/)
- **Data Handling:** Pandas, Numpy
- **PDF Generation:** ReportLab

---

## 📥 التنصيب والتشغيل
1. **تحميل المشروع:**
   ```bash
   git clone https://github.com/your-username/camera-preview.git
   cd camera-preview
   ```

2. **إنشاء البيئة الافتراضية:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **تنصيب المكتبات:**
   ```bash
   pip install -r requirements.txt
   ```

4. **إعداد قاعدة البيانات:**
   ```bash
   python manage.py migrate
   ```

5. **تشغيل المشروع:**
   ```bash
   python manage.py runserver
   ```

---

## 📂 لمحة عن هيكل المشروع
المشروع مقسم إلى تطبيقات (Apps) أساسية:
- `core/`: الإعدادات الرئيسية للمشروع.
- `scanner/`: يحتوي على محرك الفحص والرادار.
- `cctv/`: وحدة إدارة ومعاينة الكاميرات.
- `assets/`: الملفات الثابتة (Static Files).

لمزيد من التفاصيل، راجع [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md).

---

## 🤝 المساهمة
نرحب بمساهمات الجميع! يرجى قراءة [CONTRIBUTING.md](CONTRIBUTING.md) لمعرفة كيفية البدء.

---

## 📜 الترخيص
هذا المشروع مرخص تحت رخصة **MIT**. راجع ملف [LICENSE](LICENSE) للمزيد من التفاصيل.

---
**تنبيه:** هذا المشروع للأغراض التعليمية والأمنية الأخلاقية فقط. لا نتحمل مسؤولية أي استخدام غير قانوني.
