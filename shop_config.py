"""Central branding / shop-identity config.

Everything customer-facing that is *about the shop itself* (name, owner, address,
contact, social links) lives here so the whole site can be re-skinned or handed to
a new owner by editing one file. Values can be overridden by environment variables
at deploy time, which keeps real contact details out of the source tree when this
goes live on a real domain.
"""

import os


def _env(key, default):
    return os.environ.get(key, default)


SHOP = {
    "name": _env("SHOP_NAME", "Gini's Boutique"),
    "short_name": _env("SHOP_SHORT_NAME", "Gini's"),
    "tagline": _env("SHOP_TAGLINE", "Handpicked ethnic wear for the modern woman"),
    "intro": _env(
        "SHOP_INTRO",
        "Sarees, salwar suits, lehengas and everyday kurtis. Traditional craft, "
        "thoughtfully curated in West Bengal.",
    ),
    # Owner
    "owner_name": _env("SHOP_OWNER_NAME", "Benozir"),
    "owner_photo": "img/owner-benozir.jpeg",  # under static/
    "owner_note": _env(
        "SHOP_OWNER_NOTE",
        "By day I'm a teacher, and fashion has always been my hobby. Gini's Boutique grew "
        "out of that love, a way to share the sarees and suits I'm drawn to with women in "
        "our neighbourhood, and now online. Every piece here is chosen by hand, for its "
        "drape, its fabric and its finish.",
    ),
    # Location
    "address_line": _env("SHOP_ADDRESS_LINE", "Golabari"),
    "address_area": _env("SHOP_ADDRESS_AREA", "North 24 Parganas"),
    "address_state": _env("SHOP_ADDRESS_STATE", "West Bengal"),
    "address_pin": _env("SHOP_ADDRESS_PIN", "743423"),
    # Contact (placeholders — fill in real values before publishing, or set via env)
    "phone": _env("SHOP_PHONE", "+91 83349 01082"),
    "whatsapp": _env("SHOP_WHATSAPP", "+91 83349 01082"),
    "email": _env("SHOP_EMAIL", "hello@ginisboutique.in"),
    "instagram": _env("SHOP_INSTAGRAM", "ginisboutique"),
    "facebook": _env("SHOP_FACEBOOK", "ginisboutique"),
    "established": _env("SHOP_ESTABLISHED", "2024"),
    "currency": _env("SHOP_CURRENCY", "₹"),
}


def full_address():
    parts = [
        SHOP["address_line"],
        SHOP["address_area"],
        f"{SHOP['address_state']} {SHOP['address_pin']}",
    ]
    return ", ".join(p for p in parts if p)
