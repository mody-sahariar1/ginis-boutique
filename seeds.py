"""Opening-collection seed data + a `seed_data()` helper.

Kept import-light (only `models`, never `app`) so it can be called both from the
`seed.py` CLI and from app startup (auto-seed on a fresh hosted database).
"""

from models import AdminUser, Product, db

# category, name, size, material, price, qty, image, featured, description, [MRP]
CATALOG = [
    # ---------------- Sarees ----------------
    ("Sarees", "White Chanderi Silk Saree", "Free Size", "Chanderi Silk", 999, 6,
     "products/saree-chanderi-white.jpeg", True,
     "A pure ivory Chanderi silk saree with a woven golden zari border and a striped, tasselled "
     "gold pallu. Featherlight, softly lustrous and quietly regal — the timeless cream-and-gold "
     "drape, styled here with a deep-green blouse. From Gini's own collection.",
     1200),
    ("Sarees", "Amethyst Handloom Cotton Saree", "Free Size", "Handloom Cotton", 1450, 14,
     "products/saree-1.jpeg", False,
     "A soft amethyst-purple handloom saree with a fine woven motif and a warm copper-tone border. "
     "Light, breathable and easy to drape — an everyday saree that still turns heads."),
    ("Sarees", "Coral Banarasi Silk Saree", "Free Size", "Banarasi Silk", 3200, 6,
     "products/saree-2.jpeg", True,
     "Warm coral silk woven with traditional Banarasi zari buttis and a rich contrast pallu. "
     "A festive classic that carries beautifully from pujas to receptions."),
    ("Sarees", "Ivory & Gold Bridal Silk Saree", "Free Size", "Kanjeevaram Silk", 6500, 3,
     "products/saree-3.jpeg", True,
     "An ivory Kanjeevaram-style silk saree with all-over gold zari weave and a temple-motif border. "
     "Made for the bride, the mother, and every milestone in between."),
    ("Sarees", "Midnight Black Georgette Party Saree", "Free Size", "Georgette", 2400, 8,
     "products/saree-4.jpeg", True,
     "A sheer black georgette saree with delicate beaded lace on the pallu and skirt. "
     "Understated and modern — pair it with the coral blouse for a striking contrast."),
    ("Sarees", "Wine Ready-to-Wear Georgette Saree", "Free Size", "Georgette", 1250, 10,
     "products/dupatta-2.jpeg", False,
     "A plain wine-red georgette saree with a fluid, ready-to-drape fall. Minimal, elegant, and "
     "endlessly versatile — dress it up with jewellery or keep it clean for the office party."),

    # ---------------- Lehengas ----------------
    ("Lehengas", "Rani Pink Sequin Lehenga", "M", "Net", 5800, 5,
     "products/lehenga-1.jpeg", True,
     "A rani-pink net lehenga hand-worked with silver sequins and mirror detailing, finished with a "
     "matching dupatta. Built to sparkle through every sangeet and reception."),
    ("Lehengas", "Rose Pink Resham Bridal Lehenga", "M", "Net", 7200, 3,
     "products/lehenga-2.jpeg", False,
     "Deep rose net lehenga blanketed in ivory resham thread-work in a scalloped jaal pattern. "
     "A softer, romantic take on bridal wear."),
    ("Lehengas", "Wine Shimmer Sequin Lehenga", "M", "Net", 5200, 4,
     "products/lehenga-3.jpeg", True,
     "A wine sequinned lehenga with a gold-edged blouse and a sheer net dupatta with zari trim. "
     "Rich, festive, and made to move on the dance floor."),
    ("Lehengas", "Emerald & Red Banarasi Bridal Lehenga", "M", "Banarasi Silk", 9500, 2,
     "products/lehenga-4.jpeg", True,
     "A regal emerald-green Banarasi lehenga with gold botanical zari, paired with a red brocade "
     "blouse and a calligraphy-border dupatta. Our showpiece bridal set."),

    # ---------------- Salwar Kameez / Suit Sets ----------------
    ("Salwar Kameez", "Mustard Chikankari Suit Set", "L", "Cotton", 1850, 9,
     "products/salwar-1.jpeg", False,
     "A sunlit mustard kurta with fine chikankari thread-work at the yoke, paired with a soft "
     "printed cotton dupatta. Comfortable enough for a full festive day."),
    ("Salwar Kameez", "Teal Bandhani Anarkali Suit", "M", "Rayon", 2200, 7,
     "products/salwar-2.jpeg", True,
     "A teal Nayra-cut anarkali in a bandhani print with a mirror-and-thread embroidered yoke and "
     "a chiffon dupatta. Festive colour, everyday comfort."),
    ("Salwar Kameez", "Coffee Brown Embroidered Suit", "M", "Muslin", 2650, 5,
     "products/salwar-3.jpeg", False,
     "A coffee-brown muslin kurta with intricate resham and mirror embroidery down the front, "
     "finished with a blush net dupatta. Rich, warm, and beautifully detailed."),
    ("Salwar Kameez", "Rust Mirror-Work Kurta Set", "M", "Cotton Silk", 1950, 8,
     "products/dupatta-3.jpeg", False,
     "A rust cotton-silk kurta with mirror and cutwork on the sleeves and hem, styled with a "
     "gold-striped printed organza dupatta. A go-to for smaller celebrations."),

    # ---------------- Kurtis ----------------
    ("Kurtis", "Orchid Pink Chikankari Kurti", "M", "Georgette", 1150, 16,
     "products/kurti-1.jpeg", False,
     "An orchid-pink georgette kurti with all-over floral chikankari. Feather-light and elegant "
     "for work, brunch, or a quiet evening out."),
    ("Kurtis", "Ivory Chikankari Georgette Kurti", "M", "Georgette", 1250, 12,
     "products/kurti-2.jpeg", True,
     "A pure-white A-line chikankari kurti with a drawstring waist and sheer sleeves. The timeless "
     "Lucknawi piece every wardrobe deserves."),
    ("Kurtis", "Sunflower Cotton Kurta Set", "L", "Cotton", 1650, 11,
     "products/kurti-3.jpeg", True,
     "A cheerful yellow-and-white floral cotton kurta with crochet-lace trim, paired with matching "
     "straight pants. Breezy, put-together, made for the everyday."),
    ("Kurtis", "Rust Red Floral Cotton Kurti", "M", "Cotton", 899, 20,
     "products/kurti-4.jpeg", False,
     "A rust-red printed cotton kurti with a black embroidered placket and mirror buttons. "
     "Our best-value everyday piece — light, easy, and endlessly wearable."),

    # ---------------- Dupattas & Stoles ----------------
    ("Dupattas & Stoles", "Beige Kashmiri Sozni Wool Shawl", "Free Size", "Kashmiri Wool", 3400, 4,
     "products/dupatta-1.jpeg", False,
     "A camel-beige pure-wool Kashmiri shawl with hand Sozni embroidery of trailing vines and "
     "paisleys. Warm, heirloom-quality, and lovelier with every winter."),
]


def image_path(rel):
    """Served URL for a product image under static/img/."""
    return f"/static/img/{rel}"


def seed_data(admin_password="changeme123"):
    """Create the admin user + opening collection if they don't exist.

    Must be called inside an active Flask app context. Idempotent.
    """
    created = []
    if not AdminUser.query.filter_by(username="admin").first():
        admin = AdminUser(username="admin")
        admin.set_password(admin_password)
        db.session.add(admin)
        created.append("admin user")

    if Product.query.count() == 0:
        for row in CATALOG:
            cat, name, size, material, price, qty, img, featured, desc = row[:9]
            original = row[9] if len(row) > 9 else None
            db.session.add(Product(
                name=name, category=cat, size=size, material=material,
                price=float(price), original_price=float(original) if original else None,
                quantity=qty, image_url=image_path(img),
                is_featured=featured, description=desc,
            ))
        created.append(f"{len(CATALOG)} products")

    db.session.commit()
    return created
