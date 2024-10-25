from flask import Blueprint, render_template, abort, request
from app.models import Orders
from app.utils import generate_signature


order_bp = Blueprint('order', __name__)


@order_bp.route("/order/<int:order_id>")
def order_route(order_id):
    order = Orders.query.get_or_404(order_id)
    signature = generate_signature(order_id, order_bp.config["SECRET_KEY"])
    return render_template("order.html", order=order, signature=signature)

@order_bp.route("/order/paid/<int:order_id>")
def order_paid(order_id):
    signature_client = request.args.get("signature")
    signature = generate_signature(order_id, order_bp.config["SECRET_KEY"])
    if signature_client != signature:
        abort(403)
    order = Orders.query.get_or_404(order_id)
    # TODO seng mail, update order
    return render_template("paid_order.html", order=order)
