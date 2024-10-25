from flask import Flask, render_template, request, redirect, url_for, abort
from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin
from flask_migrate import Migrate

from app.extansions import db
from app.utils import generate_signature
from app.models import Product, Attributes, Orders


admin_ext = Admin(template_mode='bootstrap3')
migrate_ext = Migrate()


def create_app(testing=False):
    app = Flask(__name__)
    if testing:
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    else:
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mydatabase.db"
    app.config["SECRET_KEY"] = "TypeMeIn"
    db.init_app(app)
    migrate_ext.init_app(app, db)
    admin_ext.init_app(app)

    from app.views.static_pages import pages_bp
    from app.views.orders import order_bp
    from app.views.products import products_bp

    app.register_blueprint(pages_bp, url_prefix='')
    app.register_blueprint(order_bp, url_prefix='')
    app.register_blueprint(products_bp, url_prefix='')

    return app


app = create_app()


class MyModelView(ModelView):
    column_display_all_relations = True
    column_hide_backrefs = False


admin_ext.add_view(MyModelView(Product, db.session))
admin_ext.add_view(MyModelView(Attributes, db.session))
admin_ext.add_view(MyModelView(Orders, db.session))
