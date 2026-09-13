import os
import uuid
from datetime import datetime, timedelta

from flask import Flask, abort, flash, redirect, render_template, request, url_for
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from werkzeug.utils import secure_filename

from models import AdminUser, CustomOrderRequest, Expense, Product, Sale, db
from shop_config import SHOP, full_address

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "static", "uploads")
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp", "gif"}
MAX_UPLOAD_BYTES = 5 * 1024 * 1024


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def save_uploaded_image(file_storage):
    """Saves an uploaded image under static/uploads and returns its URL path, or None."""
    if not file_storage or not file_storage.filename:
        return None
    if not allowed_file(file_storage.filename):
        flash("Image must be png, jpg, jpeg, webp, or gif.", "error")
        return None

    ext = file_storage.filename.rsplit(".", 1)[1].lower()
    filename = secure_filename(f"{uuid.uuid4().hex}.{ext}")
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    file_storage.save(os.path.join(UPLOAD_DIR, filename))
    return url_for("static", filename=f"uploads/{filename}")


def create_app():
    app = Flask(__name__)

    is_production = os.environ.get("MODIS_ENV") == "production"
    secret_key = os.environ.get("MODIS_SECRET_KEY")
    if not secret_key:
        if is_production:
            raise RuntimeError(
                "MODIS_SECRET_KEY environment variable must be set in production."
            )
        secret_key = "dev-secret-change-me"
    app.config["SECRET_KEY"] = secret_key

    # First run on a fresh clone: the database folder and the upload folder are
    # gitignored, so create them here or SQLite cannot open its file.
    os.makedirs(os.path.join(BASE_DIR, "instance"), exist_ok=True)
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    default_db_uri = "sqlite:///" + os.path.join(BASE_DIR, "instance", "shop.db")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", default_db_uri)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["MAX_CONTENT_LENGTH"] = MAX_UPLOAD_BYTES
    app.config["SESSION_COOKIE_SECURE"] = is_production
    app.config["SESSION_COOKIE_HTTPONLY"] = True
    app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = "admin_login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(AdminUser, int(user_id))

    @app.context_processor
    def inject_shop():
        # Makes `shop` and `shop_address` available in every template.
        return {"shop": SHOP, "shop_address": full_address()}

    register_routes(app)

    with app.app_context():
        db.create_all()

    return app


def register_routes(app):
    @app.route("/")
    def index():
        featured = (
            Product.query.filter_by(is_featured=True)
            .order_by(Product.created_at.asc())
            .limit(8)
            .all()
        )
        if not featured:
            featured = Product.query.order_by(Product.created_at.desc()).limit(8).all()
        categories = [c[0] for c in db.session.query(Product.category).distinct()]
        return render_template("index.html", featured=featured, categories=categories)

    @app.route("/about")
    def about():
        return render_template("about.html")

    @app.route("/catalog")
    def catalog():
        category = request.args.get("category", "").strip()
        size = request.args.get("size", "").strip()
        max_price = request.args.get("max_price", "").strip()

        query = Product.query
        if category:
            query = query.filter(Product.category == category)
        if size:
            query = query.filter(Product.size == size)
        if max_price:
            try:
                query = query.filter(Product.price <= float(max_price))
            except ValueError:
                pass

        products = query.order_by(Product.name).all()
        categories = [c[0] for c in db.session.query(Product.category).distinct()]
        sizes = [s[0] for s in db.session.query(Product.size).distinct() if s[0]]

        return render_template(
            "catalog.html",
            products=products,
            categories=categories,
            sizes=sizes,
            selected_category=category,
            selected_size=size,
            selected_max_price=max_price,
        )

    @app.route("/product/<int:product_id>")
    def product_detail(product_id):
        product = Product.query.get_or_404(product_id)
        return render_template("product.html", product=product)

    @app.route("/contact", methods=["GET", "POST"])
    def contact():
        if request.method == "POST":
            name = request.form.get("customer_name", "").strip()
            contact_info = request.form.get("contact", "").strip()
            details = request.form.get("details", "").strip()
            if not name or not contact_info or not details:
                flash("Please fill in all fields.", "error")
            else:
                request_row = CustomOrderRequest(
                    customer_name=name, contact=contact_info, details=details
                )
                db.session.add(request_row)
                db.session.commit()
                flash("Thanks! We received your request and will get back to you.", "success")
                return redirect(url_for("contact"))
        return render_template("contact.html")

    @app.route("/admin/login", methods=["GET", "POST"])
    def admin_login():
        if request.method == "POST":
            username = request.form.get("username", "").strip()
            password = request.form.get("password", "")
            user = AdminUser.query.filter_by(username=username).first()
            if user and user.check_password(password):
                login_user(user)
                return redirect(url_for("admin_dashboard"))
            flash("Invalid credentials.", "error")
        return render_template("admin_login.html")

    @app.route("/admin/logout")
    @login_required
    def admin_logout():
        logout_user()
        return redirect(url_for("admin_login"))

    @app.route("/admin/settings", methods=["GET", "POST"])
    @login_required
    def admin_settings():
        if request.method == "POST":
            current_password = request.form.get("current_password", "")
            new_username = request.form.get("new_username", "").strip()
            new_password = request.form.get("new_password", "")
            confirm_password = request.form.get("confirm_password", "")

            if not current_user.check_password(current_password):
                flash("Current password is incorrect.", "error")
            elif new_password and new_password != confirm_password:
                flash("New password and confirmation don't match.", "error")
            elif new_password and len(new_password) < 8:
                flash("New password must be at least 8 characters.", "error")
            else:
                if new_username:
                    current_user.username = new_username
                if new_password:
                    current_user.set_password(new_password)
                db.session.commit()
                flash("Credentials updated.", "success")
                return redirect(url_for("admin_dashboard"))
        return render_template("admin_settings.html")

    @app.route("/admin")
    @login_required
    def admin_dashboard():
        products = Product.query.order_by(Product.quantity).all()
        low_stock = [p for p in products if p.is_low_stock]
        total_revenue = sum(s.total for s in Sale.query.all())
        total_expenses = sum(e.amount for e in Expense.query.all())
        pending_requests = CustomOrderRequest.query.filter_by(fulfilled=False).all()

        days = 30
        today = datetime.utcnow().date()
        date_labels = [
            (today - timedelta(days=offset)).isoformat()
            for offset in range(days - 1, -1, -1)
        ]
        revenue_by_date = {d: 0.0 for d in date_labels}
        window_start = today - timedelta(days=days - 1)
        recent_sales = Sale.query.filter(Sale.sold_at >= datetime.combine(window_start, datetime.min.time())).all()
        for sale in recent_sales:
            key = sale.sold_at.date().isoformat()
            if key in revenue_by_date:
                revenue_by_date[key] += sale.total

        return render_template(
            "admin_dashboard.html",
            products=products,
            low_stock=low_stock,
            total_revenue=total_revenue,
            total_expenses=total_expenses,
            cash_on_hand=total_revenue - total_expenses,
            pending_requests=pending_requests,
            chart_labels=date_labels,
            chart_values=[round(revenue_by_date[d], 2) for d in date_labels],
        )

    @app.route("/admin/products/new", methods=["GET", "POST"])
    @login_required
    def admin_product_new():
        if request.method == "POST":
            uploaded_url = save_uploaded_image(request.files.get("image_file"))
            image_url = uploaded_url or request.form.get("image_url", "").strip() or None
            product = Product(
                name=request.form["name"].strip(),
                category=request.form["category"].strip(),
                size=request.form.get("size", "").strip() or None,
                material=request.form.get("material", "").strip() or None,
                price=float(request.form["price"]),
                original_price=float(request.form["original_price"]) if request.form.get("original_price", "").strip() else None,
                quantity=int(request.form.get("quantity", 0)),
                image_url=image_url,
                description=request.form.get("description", "").strip() or None,
                is_featured=bool(request.form.get("is_featured")),
            )
            db.session.add(product)
            db.session.commit()
            flash("Product added.", "success")
            return redirect(url_for("admin_dashboard"))
        return render_template("admin_product_form.html", product=None)

    @app.route("/admin/products/<int:product_id>/edit", methods=["GET", "POST"])
    @login_required
    def admin_product_edit(product_id):
        product = Product.query.get_or_404(product_id)
        if request.method == "POST":
            product.name = request.form["name"].strip()
            product.category = request.form["category"].strip()
            product.size = request.form.get("size", "").strip() or None
            product.material = request.form.get("material", "").strip() or None
            product.price = float(request.form["price"])
            product.original_price = float(request.form["original_price"]) if request.form.get("original_price", "").strip() else None
            product.quantity = int(request.form.get("quantity", 0))
            product.description = request.form.get("description", "").strip() or None
            product.is_featured = bool(request.form.get("is_featured"))
            uploaded_url = save_uploaded_image(request.files.get("image_file"))
            if uploaded_url:
                product.image_url = uploaded_url
            else:
                product.image_url = request.form.get("image_url", "").strip() or None
            db.session.commit()
            flash("Product updated.", "success")
            return redirect(url_for("admin_dashboard"))
        return render_template("admin_product_form.html", product=product)

    @app.route("/admin/products/<int:product_id>/delete", methods=["POST"])
    @login_required
    def admin_product_delete(product_id):
        product = Product.query.get_or_404(product_id)
        db.session.delete(product)
        db.session.commit()
        flash("Product deleted.", "success")
        return redirect(url_for("admin_dashboard"))

    @app.route("/admin/sales/new", methods=["GET", "POST"])
    @login_required
    def admin_sale_new():
        products = Product.query.order_by(Product.name).all()
        if request.method == "POST":
            product = Product.query.get_or_404(int(request.form["product_id"]))
            qty = int(request.form["quantity"])
            if qty > product.quantity:
                flash("Not enough stock for that sale.", "error")
            else:
                sale = Sale(
                    product_id=product.id,
                    quantity=qty,
                    sale_price=float(request.form.get("sale_price") or product.price),
                )
                product.quantity -= qty
                db.session.add(sale)
                db.session.commit()
                flash("Sale recorded.", "success")
                return redirect(url_for("admin_dashboard"))
        return render_template("admin_sale_form.html", products=products)

    @app.route("/admin/expenses/new", methods=["GET", "POST"])
    @login_required
    def admin_expense_new():
        if request.method == "POST":
            expense = Expense(
                description=request.form["description"].strip(),
                amount=float(request.form["amount"]),
            )
            db.session.add(expense)
            db.session.commit()
            flash("Expense recorded.", "success")
            return redirect(url_for("admin_dashboard"))
        return render_template("admin_expense_form.html")

    @app.route("/admin/requests/<int:request_id>/fulfill", methods=["POST"])
    @login_required
    def admin_request_fulfill(request_id):
        order_request = CustomOrderRequest.query.get_or_404(request_id)
        order_request.fulfilled = True
        db.session.commit()
        return redirect(url_for("admin_dashboard"))


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
