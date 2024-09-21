from datetime import datetime
from flask_migrate import Migrate
from flask import Flask, render_template, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
app.config['SECRET_KEY'] = 'TypeMeIn'
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    photo = db.Column(db.String(200))
    product = db.Column(db.String(50))
    description = db.Column(db.String(2048))
    price = db.Column(db.Integer)
    discount = db.Column(db.Integer)
    attributes = db.relationship('Attributes', backref='product', lazy=False)
    orders = db.relationship('Orders', backref='product', lazy=True)

    def __repr__(self):
        return f'<Product {self.name}>'

class Attributes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    value = db.Column(db.String(30))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)

class Orders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    email = db.Column(db.String(50))
    status = db.Column(db.String(10))
    prod_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)

class MyModelView(ModelView):
    column_display_all_relations = True
    column_hide_backrefs = False

admin = Admin(app, name='Admin Panel', template_mode='bootstrap3')
admin.add_view(MyModelView(Product, db.session))
admin.add_view(MyModelView(Attributes, db.session))
admin.add_view(MyModelView(Orders, db.session))

@app.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/product/<int:product_id>', methods=["POST", "GET"])
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    if request.method == "POST":
        email = request.form.get('email')
        new_order = Orders(email=email, status='pending', prod_id=product_id)
        db.session.add(new_order)
        db.session.commit()
        flash('Ваш заказ успешно оформлен!', 'success')
        return render_template('buing_page.html', product=product, preorder=True)
    return render_template('buing_page.html', product=product, preorder=False)


if __name__ == '__main__':
    app.run(debug=True)