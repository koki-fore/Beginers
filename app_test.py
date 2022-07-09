import os
from flask import Flask, render_template
from flask import request
from flask_sqlalchemy import SQLAlchemy
import random
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
    

class Product():
    def __init__(self,id,title,store,num,natural_price,buy_date,create_at,User_id):
        self.id = id
        self.title = title
        self.store = store
        self.num = num
        self.natural_price = natural_price
        self.buy_date = buy_date
        self.create_at = create_at
        self.User_id = User_id

def create_test_data():
    id = random.randint(1,1010)
    title_len = random.randint(1,10)
    store_len = random.randint(1,10)
    title_format = ""
    store_format = ""
    fst = 'a'
    for i in range(title_len):
        title_format += chr(ord(fst)+random.randint(0,26))
    for i in range(store_len):
        store_format += chr(ord(fst)+random.randint(0,26))
    num = random.randint(1,100)
    natural_price = random.randint(100,2000)
    now = datetime.now()
    buy_date = now.replace(year=random.randint(1990,2022),month=random.randint(1,12),day=random.randint(1,22))
    create_at = now
    user_id = random.randint(1,1000)
    res = Product(id,title_format,store_format,num,natural_price,buy_date,create_at,user_id)
    return res


# test data
# debug
res = create_test_data()
print("id = {}".format(res.id))
print("title = {}".format(res.title))
print("store = {}".format(res.store))
print("num = {}".format(res.num))
print("natural_price = {}".format(res.natural_price))
print("buy_date = {}".format(res.buy_date))
print("create_at = {}".format(res.create_at))
print("User_id = {}".format(res.User_id))

@app.route('/', methods=['POST', 'GET'])

def index():
    return render_template('templates/index.html' )

# @app.route('/kakaku', methods=['POST', 'GET'])


if __name__ == '__main__':
    app.debug = True
    
    app.run()
