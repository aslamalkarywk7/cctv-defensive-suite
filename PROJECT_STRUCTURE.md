# 📂 CCTV Defensive Suite — project structure

This file gives a full overview of the files and folders to help developers
find their way around the codebase.

---

## 🔗 Quick links
- [🏠 Back to home](README.md)
- [📄 Contributing guide](CONTRIBUTING.md)

---

## 🏗️ Main folders

### 1. `core/` (system settings)
Django base settings and path configuration.
- `settings.py`: database, apps, and static-files settings.
- `urls.py`: the main site routing file.
- `wsgi.py` / `asgi.py`: server entry points.

### 2. `scanner/` (scanning & radar app)
Handles network scanning and discovery.
- `engines.py`: core scanning logic using Scapy and sockets.
- `views.py`: code for scan interfaces and results.
- `models.py`: database tables for discovered devices.
- `templates/`: scanner HTML views.

### 3. `cctv/` (camera management app)
Adds and previews surveillance cameras.
- `views.py`: stream-link fetching and preview logic.
- `urls.py`: camera link routes.
- `templates/`: camera view templates.

### 4. `assets/` (static files)
CSS, JavaScript, and design images.

---

## 📄 Root files
- `manage.py`: Django management tool (run, migrate, create accounts).
- `requirements.txt`: required libraries.
- `db.sqlite3`: local database (created at runtime — never committed).
- `README.md`: main project guide.
- `DEPLOY.md`: production deployment guide.

---

## 🔍 Quick code search
- **Theme/design changes:** look in `assets/`.
- **Network-scan logic:** look in `scanner/engines.py`.
- **Server settings:** look in `core/settings.py`.
- **UI:** look in each app's `templates` folder.
