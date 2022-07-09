import os
from flask import Flask, render_template
from flask import request
from flask_sqlalchemy import SQLAlchemy

from datetime import datetime
from numpy import product
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
    def __init__(self,id,title,store,num,natural_price,buy_date,create_at,User_id):
        self.id = id
        self.tile = title
        self.store = store
        self.num = num
        self.natural_price = natural_price
        self.buy_date = buy_date
        self.create_at = create_at
        self.User_id = User_id

# test data
product1 = Product(10,"title","a",1,100,2020/4/10,90,100)

@app.route('/', methods=['POST', 'GET'])

def index():
    return render_template('templates/index.html' )

# @app.route('/kakaku', methods=['POST', 'GET'])


if __name__ == '__main__':
    app.debug = True
    
    app.run()
