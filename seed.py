"""Seed Gini's Boutique with an admin login and the opening collection.

Usage: python seed.py   (safe to re-run; it skips rows that already exist)
The actual data + logic live in seeds.py so app startup can reuse them.
"""

from app import create_app
from seeds import seed_data

app = create_app()

with app.app_context():
    created = seed_data()
    if created:
        print("Seeded: " + ", ".join(created))
    else:
        print("Nothing to seed — admin and products already exist.")
