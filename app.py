from crypt import methods
import os
from flask import Flask, render_template
from flask import request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

from datetime import datetime
import pytz

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///beginners.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO']=True

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    student_id = db.Column(db.Integer)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    store = db.Column(db.String(50))
    num = db.Column(db.Integer)
    natural_price = db.Column(db.Integer)
    sell_price = db.Column(db.Integer)
    buy_date =db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now(pytz.timezone('Asia/Tokyo')))
    User_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)


@app.route('/addReceipt', methods=['GET', 'POST'])
def addReceipt():
    if request.method == 'GET':
        return render_template('addReceipt.html')
    if request.method == 'POST':
        form_title = request.form.get('title')
        form_store.form.get('store')
        form_num.form.get('num')
        form_natural_price.form.get('natural_price')
        form_buy_date/form.get('buy_date')
        product = Product(
            title=form_title,
            store=form_store,
            num=form_num,
            natural_price=form_natural_price,
            buy_date=form_buy_date
        )
        db.session.add(product)
        db.session.comit()
        return redirect(url_for('/'))


@app.route('/products')
def product_list():
    products = Product.query.all()
    return render_template('price.html', products=products)



if __name__ == '__main__':
    app.run(debug=True)