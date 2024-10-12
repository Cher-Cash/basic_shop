from flask import Flask, render_template, request, redirect, url_for, abort
from extensions import db, migrate_ext, admin_ext
from flask_admin.contrib.sqla import ModelView
from models import Product, Attributes, Orders
from utils import generate_signature


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mydatabase.db"
    app.config["SECRET_KEY"] = "TypeMeIn"
    db.init_app(app)
    migrate_ext.init_app(app)
    admin_ext.init_app(app)

    @app.route("/")
    def index():
        products = Product.query.all()
        return render_template("index.html", products=products)

    @app.route("/contact")
    def contact():
        return render_template("contact.html")

    @app.route("/about")
    def about():
        return render_template("about.html")

    @app.route("/order/<int:order_id>")
    def order_route(order_id):
        order = Orders.query.get_or_404(order_id)
        signature = generate_signature(order_id, app.config["SECRET_KEY"])
        return render_template("order.html", order=order, signature=signature)

    @app.route("/order/paid/<int:order_id>")
    def order_paid(order_id):
        signature_client = request.args.get("signature")
        signature = generate_signature(order_id, app.config["SECRET_KEY"])
        if signature_client != signature:
            abort(403)
        order = Orders.query.get_or_404(order_id)
        # TODO seng mail, update order
        return render_template("paid_order.html", order=order)

    @app.route("/product/<int:product_id>", methods=["POST", "GET"])
    def product_detail(product_id):
        product = Product.query.get_or_404(product_id)
        if request.method == "POST":
            email = request.form.get("email")
            new_order = Orders(email=email, status="pending", prod_id=product_id)
            db.session.add(new_order)
            db.session.commit()
            return redirect(url_for("order_route", order_id=new_order.id))
        return render_template("buying_page.html", product=product, preorder=False)

    return app


app = create_app()


class MyModelView(ModelView):
    column_display_all_relations = True
    column_hide_backrefs = False


admin_ext.add_view(MyModelView(Product, db.session))
admin_ext.add_view(MyModelView(Attributes, db.session))
admin_ext.add_view(MyModelView(Orders, db.session))


if __name__ == "__main__":
    app.run(debug=True)
