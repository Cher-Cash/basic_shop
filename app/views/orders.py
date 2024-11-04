from flask import Blueprint, render_template, abort, request, current_app
from app.models import Orders
from app.utils import generate_signature, send_email


order_bp = Blueprint('order', __name__)


@order_bp.route("/order/<int:order_id>")
def order_route(order_id):
    order = Orders.query.get_or_404(order_id)
    signature = generate_signature(order_id, current_app.config["SECRET_KEY"])
    return render_template("order.html", order=order, signature=signature)


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
