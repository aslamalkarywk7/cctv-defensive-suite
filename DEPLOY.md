# Deploying the project on PythonAnywhere 🚀

This guide explains how to deploy **CCTV Defensive Suite** on PythonAnywhere.

## 1. Technical requirements
*   **Recommended Python version**: `Python 3.10` or `3.11`.
*   **Framework**: `Django 5.2.x`.
*   **Database**: `SQLite3` (embedded).

## 2. Detailed deployment steps

### Step 1: Upload the code
1. Zip the project files and upload them via the **Files** tab in PythonAnywhere, or use `git clone` in a **Bash Console**.
2. Open a **Bash Console** and unzip if you uploaded a Zip file.

### Step 2: Create the virtual environment and install libraries
In the **Bash Console**, run:
```bash
# Create a virtual environment
mkvirtualenv --python=/usr/bin/python3.10 myenv

# Install the required libraries
pip install -r requirements.txt
```

### Step 3: Set up the database and static files
```bash
python manage.py migrate
python manage.py collectstatic
```

### Step 4: Set up the Web App
1. Go to the **Web** tab in PythonAnywhere.
2. Click **Add a new web app**.
3. Choose **Manual Configuration** (not Django, since it was configured manually).
4. Choose **Python 3.10**.
5. In the Web App settings:
    *   **Source code**: the full path to the project folder (e.g. `/home/yourusername/project_folder`).
    *   **Working directory**: same as the Source code path.
    *   **Virtualenv**: the environment you created (e.g. `myenv`).

### Step 5: Set up the WSGI file
In the **Web** tab, click the **WSGI configuration file** link, clear everything, and paste:
```python
import os
import sys

# Project path
path = '/home/yourusername/project_folder'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'core.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```
*(Replace `yourusername` and `project_folder` with the correct paths.)*

### Step 6: Set up static files
In the **Web** tab, scroll to **Static files** and add:
*   **URL**: `/static/`
*   **Path**: the full path to the `staticfiles` folder (created by collectstatic).

## 3. Very important notes ⚠️
1. **Local radar (Scanner)**: local-network scanning (ARP/Socket radar) may not run at full capacity on cloud servers because the environment is isolated (virtual container) — but external-IP and CVE checks work well.
2. **DEBUG**: developer mode is off (`DEBUG = False`) in settings for safe deployment.
3. **Code updates**: every time you change the code, press **Reload** in the Web tab.

---
Good luck with the launch! 👨‍💻
