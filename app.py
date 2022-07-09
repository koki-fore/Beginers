import os
from flask import Flask, render_template
from flask import request
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


@app.route('/', methods=['POST', 'GET'])

def index():
    return render_template('templates/index.html' )

# @app.route('/kakaku', methods=['POST', 'GET'])


if __name__ == '__main__':
    app.debug = True
    
    app.run()