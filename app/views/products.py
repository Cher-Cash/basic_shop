from flask import Blueprint, render_template, request, redirect, url_for
from app.models import Orders, Product
from app.extansions import db


products_bp = Blueprint('products', __name__)


@products_bp.route("/")
def index():
    products = Product.query.all()
    return render_template("index.html", products=products)


@products_bp.route("/product/<int:product_id>", methods=["POST", "GET"])
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    if request.method == "POST":
        email = request.form.get("email")
        new_order = Orders(email=email, status="pending", prod_id=product_id)
        db.session.add(new_order)
        db.session.commit()
        return redirect(url_for("order.order_route", order_id=new_order.id))
    return render_template("buying_page.html", product=product, preorder=False)