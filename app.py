import os
from flask import Flask, render_template
from flask import request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

from datetime import datetime
import pytz

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///beginners.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO']=True
app.config['SECRET_KEY'] = os.urandom(24)

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False)
    student_id = db.Column(db.String(4))
    password = db.Column(db.String(12))


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    store = db.Column(db.String(50))
    num = db.Column(db.Integer)
    natural_price = db.Column(db.Integer)
    sell_price = db.Column(db.Integer)
    buy_date =db.Column(db.String(30))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now(pytz.timezone('Asia/Tokyo')))
    # User_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
db.create_all()

@app.route('/products')
def product_list():
    products = Product.query.all()
    return render_template('price.html', products=products)

@app.route('/addReceipt', methods=['GET', 'POST'])
def addReceipt():
    if request.method == 'GET':
        return render_template('addReceipt.html')
    if request.method == 'POST':
        form_title = request.form.get('title')
        form_store=request.form.get('store')
        form_num=request.form.get('num')
        form_natural_price=request.form.get('natural_price')
        form_buy_date=request.form.get('buy_date')
        form_sell_price=request.form.get('sell_price')

        product = Product(
            buy_date=form_buy_date,
            store=form_store,
            title=form_title,
            num=form_num,
            natural_price=form_natural_price,
            sell_price=form_sell_price
            
        )
        db.session.add(product)
        db.session.commit()
        return redirect(url_for('product_list'))




@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        student_id = request.form.get('student_id')
        password = request.form.get('password')

        user = User(username=username, student_id=student_id, 
                    password=generate_password_hash(password, method='sha256'))

        db.session.add(user)
        db.session.commit()
        return redirect('/login')
    else:
        return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        student_id = request.form.get('student_id')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if check_password_hash(user.password, password):
            login_user(user)
            return redirect('/addReceipt')
    else:
        return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)