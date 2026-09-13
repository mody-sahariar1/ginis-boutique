from datetime import datetime

from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

db = SQLAlchemy()

LOW_STOCK_THRESHOLD = 5


class AdminUser(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    category = db.Column(db.String(60), nullable=False)
    size = db.Column(db.String(20), nullable=True)
    material = db.Column(db.String(80), nullable=True)
    price = db.Column(db.Float, nullable=False)            # selling price
    original_price = db.Column(db.Float, nullable=True)    # MRP / struck-through price
    quantity = db.Column(db.Integer, nullable=False, default=0)
    image_url = db.Column(db.String(255), nullable=True)
    description = db.Column(db.Text, nullable=True)
    is_featured = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def is_on_sale(self):
        return bool(self.original_price and self.original_price > self.price)

    @property
    def discount_pct(self):
        if self.is_on_sale:
            return round((1 - self.price / self.original_price) * 100)
        return 0

    sales = db.relationship("Sale", backref="product", lazy=True)

    @property
    def is_low_stock(self):
        return self.quantity <= LOW_STOCK_THRESHOLD

    @property
    def units_sold(self):
        return sum(s.quantity for s in self.sales)


class Sale(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    sale_price = db.Column(db.Float, nullable=False)
    sold_at = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def total(self):
        return self.quantity * self.sale_price


class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(255), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    incurred_at = db.Column(db.DateTime, default=datetime.utcnow)


class CustomOrderRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(120), nullable=False)
    contact = db.Column(db.String(120), nullable=False)
    details = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    fulfilled = db.Column(db.Boolean, default=False)
