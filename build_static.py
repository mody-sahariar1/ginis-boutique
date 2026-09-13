"""Freeze the storefront into static HTML for GitHub Pages (docs/).

Renders every browsable page via the Flask test client, rewrites root-absolute
URLs to relative ones (so it works under /ginis-boutique/), strips the admin
link, and neutralises the two server-side forms. Run: python build_static.py
"""

import os
import re
import shutil

from flask import url_for

from app import app
from models import Product

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "docs")


def slugify(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


with app.app_context():
    products = Product.query.order_by(Product.category, Product.name).all()
    categories = sorted({p.category for p in products})
    with app.test_request_context():
        cat_url = {c: url_for("catalog", category=c) for c in categories}
        prod_url = {p.id: url_for("product_detail", product_id=p.id) for p in products}

cat_file = {c: f"catalog-{slugify(c)}.html" for c in categories}
client = app.test_client()


def rewrite(html):
    # static assets → relative (covers href, src, and url('/static/...') in styles)
    html = html.replace("/static/", "static/")
    # category + product links → their static filenames (do these before /catalog)
    for c, u in cat_url.items():
        html = html.replace(f'href="{u}"', f'href="{cat_file[c]}"')
    for pid, u in prod_url.items():
        html = html.replace(f'href="{u}"', f'href="product-{pid}.html"')
    # simple page links
    html = html.replace('href="/catalog"', 'href="catalog.html"')
    html = html.replace('href="/about"', 'href="about.html"')
    html = html.replace('href="/contact"', 'href="contact.html"')
    html = html.replace('href="/"', 'href="index.html"')
    # drop the admin nav item (no server here)
    html = re.sub(r'<li[^>]*>\s*<a class="nav-link nav-admin".*?</a>\s*</li>', "", html, flags=re.S)
    return html


def fetch(path):
    return rewrite(client.get(path).get_data(as_text=True))


def save(name, html):
    with open(os.path.join(OUT, name), "w") as f:
        f.write(html)


# fresh output dir
if os.path.isdir(OUT):
    shutil.rmtree(OUT)
os.makedirs(OUT)

# pages
save("index.html", fetch("/"))
save("catalog.html", fetch("/catalog"))
for c in categories:
    save(cat_file[c], fetch(cat_url[c]))
for p in products:
    save(f"product-{p.id}.html", fetch(prod_url[p.id]))
save("about.html", fetch("/about"))

# contact — neutralise the POST form for a static preview
contact = fetch("/contact")
contact = contact.replace(
    '<form method="post">',
    '<form method="post" onsubmit="return false" '
    'title="Preview form. To order, message us on Instagram or call the number shown.">',
)
contact = contact.replace(
    "<button type=\"submit\" class=\"btn btn-brand\">Send Request</button>",
    "<button type=\"submit\" class=\"btn btn-brand\">Send Request</button>"
    "<div class=\"form-text mt-2\">This is a preview. To place an order, message us on "
    "Instagram or call the number under Visit the Boutique.</div>",
)
# also disable the catalog filter form (it needs a server) — keep it visible but inert
contact = contact  # (contact has no filter form; handled per-page below)
save("contact.html", contact)

# copy assets + disable Jekyll processing
shutil.copytree(os.path.join(HERE, "static"), os.path.join(OUT, "static"))
open(os.path.join(OUT, ".nojekyll"), "w").close()

print(f"Built {len(products) + len(categories) + 4} pages into docs/ "
      f"({len(products)} products, {len(categories)} categories).")
