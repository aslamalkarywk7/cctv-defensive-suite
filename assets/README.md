# 👁️ Karioka Intelligence Surveillance System
### Advanced AI-Powered Camera Scanning & Exploitation Framework

نظام **Karioka** هو أداة استخباراتية متطورة مبنية بلغة Python وإطار عمل Django، مصممة لفحص الشبكات، اكتشاف كاميرات المراقبة، واختبار اختراقها باستخدام تقنيات الذكاء الاصطناعي وثغرات يوم الصفر (Zero-Day exploits).

---

## 🚀 المميزات الرئيسية (Core Features)

*   **🛰️ Stealth ARP Radar:** اكتشاف فوري للكاميرات في الشبكة المحلية مع تحديد نوع الجهاز (Vendor) بناءً على الماك أدريس (MAC Address).
*   **🧨 CVE-2018-9995 Exploit:** هجوم مخصص لاستخراج بيانات الاعتماد (Credentials) مباشرة من أجهزة DVR/TVT و Dahua.
*   **🧠 AI Image Analysis:** فحص تلقائي للصور الملتقطة باستخدام خوارزميات OpenCV لتحديد جودة الرؤية (Clear vs Blurry).
*   **⚡ Async Brute Force:** محرك تخمين كلمات مرور فائق السرعة يعتمد على `httpx` و `asyncio`.
*   **📊 Military-Grade Reporting:** تصدير تقارير استخباراتية مفصلة بصيغ PDF و Excel (XLSX).
*   **🛡️ Stealth Discovery:** دعم بروتوكولات UPnP و SSDP لاكتشاف الأجهزة المخفية.

---

## 🛠️ التقنيات المستخدمة (Tech Stack)

- **Backend:** Django (Python Framework)
- **Networking:** Scapy, Httpx, Requests
- **CV/AI:** OpenCV (cv2), Numpy
- **Reporting:** ReportLab (PDF), Pandas (Excel)
- **Database:** SQLite3

---

## 📂 لقطة من هيكل المشروع
- `scanner/engines.py`: المحرك الأساسي للاختراق والمسح.
- `scanner/views.py`: التحكم في واجهة المستخدم ومعالجة البيانات.
- `scanner/models.py`: قاعدة بيانات النتائج والمخترقات.

---

## ⚠️ إخلاء مسؤولية (Disclaimer)
هذه الأداة مصممة لأغراض **الأمن السيبراني التعليمي واختبار الاختراق الأخلاقي فقط**. الاستخدام غير المصرح به ضد أجهزة لا تملك الإذن لفحصها يقع تحت مسؤوليتك القانونية الكاملة.

---

## 👤 المطور
تم تطوير هذا المشروع كجزء من أبحاث الأمن الرقمي المتقدمة.
