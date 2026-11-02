"""Central branding / shop-identity config.

Everything customer-facing that is *about the shop itself* (name, owner, address,
contact, social links) lives here so the whole site can be re-skinned or handed to
a new owner by editing one file. Values can be overridden by environment variables
at deploy time, which keeps real contact details out of the source tree when this
goes live on a real domain.
"""

import os
from urllib.parse import quote


def _env(key, default):
    return os.environ.get(key, default)


SHOP = {
    "name": _env("SHOP_NAME", "Gini's Boutique"),
    "short_name": _env("SHOP_SHORT_NAME", "Gini's"),
    "tagline": _env("SHOP_TAGLINE", "Good clothes, close to home"),
    "intro": _env(
        "SHOP_INTRO",
        "Sarees, kurti sets, suits and gowns chosen by Benozir for women in and around "
        "Golabari, so a good outfit on a fair budget does not need a long journey.",
    ),
    # Owner
    "owner_name": _env("SHOP_OWNER_NAME", "Benozir"),
    "owner_photo": "img/benozir-portrait-2.jpg",  # under static/
    "owner_note": _env(
        "SHOP_OWNER_NOTE",
        "In a village, wanting something beautiful can feel like asking for too much. "
        "Benozir, who has loved clothes all her life, saw how far women had to travel and "
        "how carefully they had to count. So she opened a small shop of her own, for them.",
    ),
    # Location
    "address_line": _env("SHOP_ADDRESS_LINE", "Near Golabari Pallimangal School and Taki Road, Golabari"),
    "address_area": _env("SHOP_ADDRESS_AREA", "P.O. Golabari Bazar, P.S. Shasan, North 24 Parganas"),
    "address_state": _env("SHOP_ADDRESS_STATE", "West Bengal"),
    "address_pin": _env("SHOP_ADDRESS_PIN", "743423"),
    # Contact. Email and social links stay hidden until they are real (set via env).
    "phone": _env("SHOP_PHONE", "+91 83349 01082"),
    "whatsapp": _env("SHOP_WHATSAPP", "+91 83349 01082"),
    "email": _env("SHOP_EMAIL", ""),
    "instagram": _env("SHOP_INSTAGRAM", ""),
    "facebook": _env("SHOP_FACEBOOK", ""),
    "established": _env("SHOP_ESTABLISHED", "2024"),
    "currency": _env("SHOP_CURRENCY", "₹"),
}


def whatsapp_url(message=""):
    """A wa.me link to the shop's WhatsApp, with the customer's message ready to send."""
    digits = "".join(ch for ch in SHOP["whatsapp"] if ch.isdigit())
    query = f"?text={quote(message)}" if message else ""
    return f"https://wa.me/{digits}{query}"


def full_address():
    parts = [
        SHOP["address_line"],
        SHOP["address_area"],
        f"{SHOP['address_state']} {SHOP['address_pin']}",
    ]
    return ", ".join(p for p in parts if p)
