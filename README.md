# MODI'S CLOTHS SHOP

A smart shop management + e-commerce site: product catalog for customers, and an
admin dashboard for inventory, sales, expenses, and custom order requests.

## Setup

```powershell
cd C:\Users\saiqu\Projects\MODIs
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python seed.py      # creates admin user (admin / changeme123) and sample products
python app.py        # runs at http://127.0.0.1:5000
```

**Change the seeded admin password** after first login — go to **Settings** in
the nav bar once logged in.

## Structure

- `app.py` — Flask routes (catalog, product detail, contact/custom order form,
  admin login/settings, admin dashboard, product/sale/expense CRUD, image upload)
- `wsgi.py` — production entry point (`gunicorn wsgi:app`)
- `Procfile` — process declaration for Heroku-style hosts (Render, Railway, etc.)
- `models.py` — SQLAlchemy models: `Product`, `Sale`, `Expense`,
  `CustomOrderRequest`, `AdminUser`
- `templates/` — Jinja2 templates (Bootstrap 5 + Chart.js via CDN)
- `static/` — CSS/JS assets; `static/uploads/` holds uploaded product images
  (gitignored except for a `.gitkeep`)
- `instance/shop.db` — SQLite database (created on first run, gitignored)
- `seed.py` — one-time admin user + sample product seeding

## What's implemented (MVP)

- Public catalog with category / size / max-price filters
- Product detail pages
- Custom order request form (saved to DB, visible in admin dashboard)
- Admin login + settings page (change username/password yourself, never share
  it in chat or with anyone else)
- Admin dashboard: revenue / expenses / cash-on-hand summary, low-stock
  alerts, 30-day sales chart, inventory table, pending custom order requests
- Product CRUD with image upload (png/jpg/jpeg/webp/gif, 5MB max) or image URL
- Sale recording (decrements stock), expense recording

## Deployment

The app reads its production config from environment variables — nothing
sensitive is hardcoded:

- `MODIS_ENV=production` — enables production mode (secure session cookies,
  and requires `MODIS_SECRET_KEY` to be set or the app refuses to start)
- `MODIS_SECRET_KEY` — a long random string; generate one with
  `python -c "import secrets; print(secrets.token_hex(32))"`
- `DATABASE_URL` — optional, defaults to the local SQLite file; point this at
  a hosted Postgres URL if you outgrow SQLite

To deploy on a typical host (Render, Railway, Fly.io, etc.):

1. Push this project to a git repo the host can pull from.
2. Set `MODIS_ENV`, `MODIS_SECRET_KEY` (and `DATABASE_URL` if using Postgres)
   as environment variables in the host's dashboard.
3. The host should detect `Procfile` / `wsgi:app` and run
   `gunicorn wsgi:app` automatically (gunicorn only runs on Linux, so this
   step happens on the host, not on your Windows machine).
4. Run `seed.py` once against the deployed environment (most hosts offer a
   one-off shell/console command for this) to create your first admin login.

You (not me) choose and sign up for the actual hosting provider — I can
prepare the app's config for whichever one you pick, but account creation and
billing decisions are yours to make.

## Possible next steps

- Multi-admin / staff roles
- Product demand/analytics beyond the revenue chart (best sellers, low
  movers)
- Move off SQLite to Postgres once there's real traffic
