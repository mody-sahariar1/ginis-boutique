# Gini's Boutique

A women's traditional ethnic-wear boutique: an elegant storefront (sarees,
salwar kameez, lehengas, kurtis, dupattas) for customers, plus an admin
dashboard for inventory, sales, expenses, and custom-order requests.

Founder: **Benozir** · Golabari, North 24 Parganas, West Bengal 743423.

## Deploy the live site (one click)

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/mody-sahariar1/ginis-boutique)

Click the button, sign in to Render (free), and it reads `render.yaml` to build and
launch the site at a public `…onrender.com` URL — the database auto-seeds the opening
collection on first boot. To make that live site private, add a `SITE_PASSWORD`
environment variable in the Render dashboard (view username defaults to `gini`).

## Setup (run locally)

```bash
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python seed.py      # creates admin (admin / changeme123) + the opening collection
python app.py       # runs at http://127.0.0.1:5000
```

**Change the seeded admin password** after first login — go to **Settings** in
the nav bar once logged in.

## Make it yours (branding in one place)

All shop identity — name, tagline, owner bio, address, phone, email, social
handles — lives in **`shop_config.py`** and is injected into every template as
`shop.*`. Change the boutique's name or hand it to a new owner by editing that
one file (or by overriding the matching `SHOP_*` environment variables at
deploy time, which keeps real phone/email out of the source tree). The theme
palette and fonts are single-sourced too, as CSS variables at the top of
`static/css/style.css`.

Product photos live under `static/img/products/` and are seeded in `seed.py`;
the owner portrait is `static/img/owner-benozir.jpeg`.

**Change the seeded admin password** after first login — go to **Settings** in
the nav bar once logged in.

## Structure

- `app.py` — Flask routes (home, catalog, product detail, our-story, contact/
  custom-order form, admin login/settings, dashboard, product/sale/expense CRUD)
- `shop_config.py` — **single source of truth for all branding** (name, owner,
  address, contact, socials); overridable via `SHOP_*` env vars
- `wsgi.py` — production entry point (`gunicorn wsgi:app`)
- `Procfile` — process declaration for Heroku-style hosts (Render, Railway, etc.)
- `models.py` — SQLAlchemy models: `Product` (now with `description` +
  `is_featured`), `Sale`, `Expense`, `CustomOrderRequest`, `AdminUser`
- `templates/` — Jinja2 templates (Bootstrap 5); `_product_card.html` is the
  reusable product tile; `base.html` carries the boutique nav + footer
- `static/css/style.css` — theme tokens (palette + fonts) at the top
- `static/img/` — hero + product photography; `static/uploads/` holds
  admin-uploaded product images (gitignored except a `.gitkeep`)
- `instance/shop.db` — SQLite database (created on first run, gitignored)
- `seed.py` — admin user + the opening collection (18 pieces)

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
