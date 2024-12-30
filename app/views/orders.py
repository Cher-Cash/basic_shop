from flask import Blueprint, render_template, abort, request, current_app, redirect
from app.models import Orders, Product
from app.utils import generate_signature, send_email


order_bp = Blueprint('order', __name__)


@order_bp.route("/order/<int:order_id>")
def order_route(order_id):
    order = Orders.query.get_or_404(order_id)
    signature = generate_signature(order_id, current_app.config["SECRET_KEY"])
    return render_template("order.html", order=order, signature=signature)


@order_bp.route("/order/paying/<int:order_id>")
def order_paying(order_id):
    order = Orders.query.get_or_404(order_id)
    product = Product.query.get_or_404(order.prod_id)
    price = product.price
    signature = generate_signature(order_id, current_app.config["SECRET_KEY"])
    callback_url = f"https://bshop.gunlinux.ru/order/paid/{order.id}"
    redirectional_url = f"https://pay.gunlinux.ru/process?company_id=1&order_id={order.id}&callback_url={callback_url}&price={price}"
    return redirect(redirectional_url)

@order_bp.route("/order/paid/<int:order_id>")
def order_paid(order_id):
    signature_client = request.args.get("signature")
    signature = generate_signature(order_id, current_app.config["SECRET_KEY"])
    if signature_client != signature:
        abort(403)
    current_order = Orders.query.get_or_404(order_id)
    print(type(current_order))
    # TODO seng mail, update order
    send_email(current_order)
    return render_template("paid_order.html", order=current_order)
