"""Run once to create the admin login and a few sample products.

Usage: python seed.py
"""

from app import create_app
from models import AdminUser, Product, db

app = create_app()

with app.app_context():
    if not AdminUser.query.filter_by(username="admin").first():
        admin = AdminUser(username="admin")
        admin.set_password("changeme123")
        db.session.add(admin)
        print("Created admin user -> username: admin / password: changeme123 (change this!)")
    else:
        print("Admin user already exists.")

    if Product.query.count() == 0:
        sample_products = [
            Product(name="Kids Cotton Frock", category="Kids Wear", size="4-5Y",
                    material="Cotton", price=499.0, quantity=12),
            Product(name="School Uniform Shirt", category="Uniforms", size="M",
                    material="Poly-Cotton", price=350.0, quantity=20),
            Product(name="Boys Sports Kit", category="Sports Kits", size="L",
                    material="Polyester", price=899.0, quantity=4),
            Product(name="Men's Casual Shirt", category="Shirts", size="XL",
                    material="Cotton", price=699.0, quantity=15),
        ]
        db.session.add_all(sample_products)
        print(f"Added {len(sample_products)} sample products.")
    else:
        print("Products already exist, skipping sample data.")

    db.session.commit()
