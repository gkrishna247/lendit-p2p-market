# LendIt — P2P Rental Marketplace

A Peer-to-Peer (P2P) item rental marketplace built with Django. Users can list items they own for rent and book items from other users. The entire application (frontend + backend) runs on a single Django server.

## Features

- **User Authentication**: Register, login, and logout
- **Item Listings**: List items for rent with title, description, and daily price
- **Browse & Search**: View all available items in a clean card layout
- **Booking System**: Request to rent items with date-based pricing
- **Dashboard**: Manage your listings and respond to booking requests
- **Booking Management**: Approve or reject incoming booking requests

## Tech Stack

| Component | Technology |
|---|---|
| Language | Python 3.10+ |
| Framework | Django 5.x |
| Database | SQLite |
| Frontend | HTML5, CSS3, JavaScript |
| Templates | Django Template Language |
| Config | python-decouple |
| Static Files | WhiteNoise |

## Project Structure

```
lendit-p2p-market/
├── config/                  # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── marketplace/             # Main application
│   ├── models.py            # Item & Booking models
│   ├── views.py             # All views (function-based)
│   ├── forms.py             # Registration, Item, Booking forms
│   ├── urls.py              # URL patterns
│   └── admin.py             # Admin configuration
├── templates/               # HTML templates
│   ├── base.html
│   ├── navbar.html
│   ├── home.html
│   └── marketplace/
├── static/                  # CSS & JS source files
│   ├── css/style.css
│   └── js/main.js
├── manage.py
├── requirements.txt         # For PythonAnywhere (pip)
└── pyproject.toml           # uv project config
```

## Local Development Setup

### Prerequisites
- Python 3.10+
- [uv](https://docs.astral.sh/uv/) package manager

### Steps

1. **Clone the repository**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/lendit-p2p-market.git
   cd lendit-p2p-market
   ```

2. **Install dependencies with uv**:
   ```bash
   uv sync
   ```

3. **Create your `.env` file**:
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and set a proper `SECRET_KEY`.

4. **Run migrations**:
   ```bash
   uv run python manage.py migrate
   ```

5. **Create a superuser** (optional, for admin access):
   ```bash
   uv run python manage.py createsuperuser
   ```

6. **Collect static files**:
   ```bash
   uv run python manage.py collectstatic --noinput
   ```

7. **Start the development server**:
   ```bash
   uv run python manage.py runserver
   ```

8. Open your browser at **http://127.0.0.1:8000/**

## PythonAnywhere Deployment

### 1. Upload Your Code

Push to GitHub and clone on PythonAnywhere:
```bash
git clone https://github.com/YOUR_USERNAME/lendit-p2p-market.git
```

### 2. Create a Virtual Environment

```bash
cd lendit-p2p-market
python3.10 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the project root:
```
SECRET_KEY=your-production-secret-key
DEBUG=False
ALLOWED_HOSTS=yourusername.pythonanywhere.com
```

> **Tip**: Generate a secure key with:
> ```python
> from django.core.management.utils import get_random_secret_key
> print(get_random_secret_key())
> ```

### 4. Run Migrations & Collect Static Files

```bash
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

### 5. Configure the Web App

In the PythonAnywhere **Web** tab:

- **Source code**: `/home/yourusername/lendit-p2p-market`
- **Virtualenv**: `/home/yourusername/lendit-p2p-market/.venv`

Edit the **WSGI configuration file** and replace its content with:
```python
import os
import sys

path = '/home/yourusername/lendit-p2p-market'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

### 6. Configure Static Files

In the **Static files** section of the Web tab:

| URL | Directory |
|---|---|
| `/static/` | `/home/yourusername/lendit-p2p-market/staticfiles` |

### 7. Reload

Click **Reload** on the Web tab. Your app should be live!

## Admin Access

Visit `/admin/` and log in with your superuser credentials to manage items and bookings.

## License

MIT
