# 🛡️ CCTV Defensive Suite — Camera Inventory & Network Auditing (Django)

A Django-based system for **defensive** management and review of CCTV cameras
and local networks: device inventory, exposure review, known-vulnerability
(CVE) lookup, and organized stream preview — built for auditors securing
their own infrastructure.

---

## 🚀 Quick links
- [📄 Contributing guide (CONTRIBUTING.md)](CONTRIBUTING.md)
- [⚖️ License (LICENSE)](LICENSE)
- [📂 Detailed project structure (PROJECT_STRUCTURE.md)](PROJECT_STRUCTURE.md)
- [🛠️ Deployment guide (DEPLOY.md)](DEPLOY.md)

---

## ✨ Key features
- **Network radar:** discover devices on the local network via ARP and sockets.
- **Camera manager:** add, edit, and preview cameras in one inventory.
- **Vulnerability lookup:** match discovered devices against known CVEs.
- **Professional reports:** export audit findings as PDF.
- **Modern UI:** responsive interface for desktop and mobile.

---

## 🛠️ Tech stack
- **Backend:** [Django 5.x](https://www.djangoproject.com/)
- **Image Processing:** [OpenCV](https://opencv.org/)
- **Networking:** [Scapy](https://scapy.net/), [Requests](https://requests.readthedocs.io/)
- **Data Handling:** Pandas, Numpy
- **PDF Generation:** ReportLab

---

## 📥 Install & run
1. **Clone the project:**
   ```bash
   git clone https://github.com/aslamalkarywk7/cctv-defensive-suite.git
   cd cctv-defensive-suite
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the database:**
   ```bash
   python manage.py migrate
   ```

5. **Run the project:**
   ```bash
   python manage.py runserver
   ```

---

## 📂 Project structure at a glance
The project is split into core apps:
- `core/`: main project settings.
- `scanner/`: scanning and radar engine.
- `cctv/`: camera management and preview module.
- `assets/`: static files.

See [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) for details.

---

## 🤝 Contributing
Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) to get started.

---

## 📜 License
This project is licensed under the **MIT** license. See [LICENSE](LICENSE) for details.

---
**Notice:** for educational and ethical defensive-security use only — audit only networks and devices you own or are authorized to test.
