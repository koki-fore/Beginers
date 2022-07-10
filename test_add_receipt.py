import os
from flask import Flask, render_template
from flask import request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

from datetime import datetime
import pytz

from datetime import datetime
import locale
from pathlib import Path
import re
from pandas import to_numeric
import sys

########################################################
# Get date time information
def Get_date_time(date_str,date_format):
    try:
        res_date = datetime.strptime(date_str,date_format)
        return True
    except:
        return False

# 曜日を除外した日付の文字列を生成
def to_easy_date(date_str):
    first_separate = date_str.split("(")
    if(len(first_separate) < 2):
        return False
    second_separate = first_separate[1].split(")")
    second_space_separate = second_separate[1].split(" ")
    first_space_split = first_separate[0].split(" ")
    date_type = ""
    for it in first_space_split:
        date_type += it
    second_start = 0
    if(len(second_space_separate) > 1):
        while(second_start < len(second_space_separate[1]) and second_space_separate[1][second_start].isnumeric() == False):
            second_start += 1
    first_start = 0
    while(first_start < len(date_type) and date_type[first_start].isnumeric() == False):
        first_start += 1
    res = date_type[first_start:]
    if(len(second_space_separate) > 1):
        if(len(second_space_separate[1][second_start:]) > 0):
            res += " "+second_space_separate[1][second_start:]
    return res

def answer_type_date(date_str,date_format):
    # 日付の出力形式
    answer_type = "%Y/%m/%d %H:%M"
    res_date = datetime.strptime(date_str,date_format)
    res = datetime.strftime(res_date,answer_type)
    return res

def Get_date_format(date_separates):
    year = ["%y", "%Y"]
    month = ["%m"]
    day = ["%d"]
    date_format = [year,month,day]
    res = []
    for now_index, now_element in enumerate(date_separates):
        now_len = int(len(now_element))
        for bit in range(2**now_len):
            flag = True
            now_format = ""
            for index, element in enumerate(date_format):
                element_access = (bit << index) & 1
                if(element_access < len(element)):
                    now_format += element[element_access]
                    if(index < now_len):
                        now_format += now_element[index]
                else:
                    flag = False
                    break
            if(flag == True):
                res.append(now_format)
    return res

def Get_time_format(time_separates):
    hour = ["%H"]
    minute = ["%M"]
    time_format = [hour,minute]
    res = []
    for now_index, now_element in enumerate(time_separates):
        now_len = int(len(now_element))
        for bit in range(2**now_len):
            now_format = ""
            flag = True
            for index, element in enumerate(time_format):
                element_access = (bit << index) & 1
                if(element_access < len(element)):
                    now_format += element[element_access]
                    if(index < now_len):
                        now_format += now_element[index]
                else:
                    flag = False
                    break
            if(flag == True):
                res.append(now_format)
    return res

def Get_english_date(date_str):
    # Get English datetime
    date_separates = [
        ["",""],
        ["-","-"],
        ["/","/"]
    ]
    date_formats = Get_date_format(date_separates)
    time_separates = [[":"]]
    time_formats = Get_time_format(time_separates)
    for now_date in date_formats:
        for now_time in time_formats:
            now_format = now_date+" "+now_time
            if(Get_date_time(date_str,now_format) == True):
                return answer_type_date(date_str,now_format)
            elif(Get_date_time(date_str,now_date)  == True):
                return answer_type_date(date_str,now_date)
    return False

def Get_japanese_date(date_str):
    # locale.setlocale(locale.LC_TIME,'ja_JP.UTF-8')
    date_separates = [
        ["年","月","日"],
    ]
    time_separates = [
        ["時","分"],
        [":"]
    ]
    date_formats = Get_date_format(date_separates)
    time_formats = Get_time_format(time_separates)
    for now_date in date_formats:
        for now_time in time_formats:
            now_format = now_date+" "+now_time
            if(Get_date_time(date_str,now_format) == True):
                return answer_type_date(date_str,now_format)
            elif(Get_date_time(date_str,now_date) == True):
                return answer_type_date(date_str,now_date)
    return False


def parse_date_time(date_str):
    easy_date = to_easy_date(date_str)
    if(easy_date == False):
        return False
    res = Get_english_date(easy_date)
    if(res == False):
        return Get_japanese_date(easy_date)
    else:
        return res

def Get_true_date(data,end):
    for it in range(end):
        now = parse_date_time(data[it])
        if(now != False):
            return now
    return False
########################################################

########################################################
# Get price of item.
def create_price_format():
    pre_type = ["\\","*"]
    after_type = ["込","非"]
    return pre_type,after_type


def is_price(price_str):
    pre_format, after_format = create_price_format()
    for pre in pre_format:
        if(price_str[:len(pre)] == pre and len(re.findall(r'\d+',price_str)) > 0):
            return True
    
    for after in after_format:
        if(price_str[-len(after):] == after and len(re.findall(r'\d+',price_str)) > 0):
            return True
    return False

def to_easy_price(price_str):
    now = price_str.split(" ")
    next = [x for x in now if(x != '')]
    return next


def create_cnt_format():
    pre_type = ["×"]
    after_type = ["個","コ"]
    return pre_type,after_type

def is_cnt(str):
    pre_format, after_format = create_cnt_format()
    for pre in pre_format:
        if(str[:len(pre)] == pre):
            return True
    
    for after in after_format:
        if(str[-len(after):] == after):
            return True
    return False

def get_price(price_str):
    easy_price = to_easy_price(price_str)
    item_name = ""
    cnt = 1
    price = -1
    for now in easy_price:
        if(is_price(now) == True):
            nums = re.findall(r'\d+',now)
            price = 0
            for i in nums:
                price *= 1000
                price += to_numeric(i)
        else:
            if(is_cnt(now) == True):
                cnt_list = re.findall(r'\d+',now)
                cnt = 0
                for now_cnt in cnt_list:
                    cnt *= 1000
                    cnt += to_numeric(now_cnt)
            else:
                item_name += now
    # 商品名，価格，個数
    return [item_name,price,cnt]

########################################################
# Get price data range
def is_sum(price_str_list):
    sum_type = [["合","小","全"],["計","体"]]
    flags = [False,False]
    for index, element in enumerate(price_str_list):
        for flag_index in range(len(flags)):
            if(flags[flag_index] == True):
                continue
            for it in sum_type[flag_index]:
                if(it in element):
                    flags[flag_index] = True
    for it in flags:
        if(it == False):
            return False
    return True

def get_price_range(data):
    start = 0
    end = 0
    price_format = create_price_format()
    for index, element in enumerate(data):
        now = to_easy_price(element)
        if(is_sum(now) == True and end == 0):
            end = index
        if(start != 0):
            continue
        for now_c in now:
            if(is_price(now_c) == True):
                start = index
    return start,end

def discount_name(price_str):
    discount_format = ["値引","割引"]
    for now_discount in discount_format:
        if(now_discount in price_str):
            return True
    return False

def except_price_name(item_name):
    except_format = ["消費税"]
    for now_except in except_format:
        if(now_except in item_name):
            return True
    return False

########################################################
# Get all value
def Get_all_price_value(data):
    start, end = get_price_range(data)
    res = []
    for it in range(start,end):
        now_res = get_price(data[it])
        if(len(res) > 0 and res[-1][1] == -1):
            res[-1][2] = now_res[2]
            if(res[-1][1] < now_res[1]):
                res[-1][1] = now_res[1]
        elif(discount_name(now_res[0]) == False and except_price_name(now_res[0]) == False):
            res.append(now_res)
    return res

def Get_true_price_all_value(data):
    answer_data = Get_all_price_value(data)
    res = []
    for now in answer_data:
        if(now[1] == -1):
            continue
        res.append(now)
    return res


########################################################
# Get all Value
def Get_all_value(data):
    start,end = get_price_range(data)
    date_value = Get_true_date(data,start)
    price_answer = Get_true_price_all_value(data)
    if(date_value == False):
        date_value = None
    return date_value,price_answer


args = sys.argv
test_path = args[1]

buy_date = None
price_data = []
with open( test_path,"r") as f:
    reader = f.read().split("\n")
    buy_date, price_data = Get_all_value(reader)

# test = ["2020年5月10日 14時00分","2020510 14:00","2020/5/10 14:00","2020-5-10 14:00"]
# test = ["2020年5月10日 (土)14時00分","2020510 (Sat)14:00"]



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
        if(len(price_data) > 0):
            return render_template('/addReceipt',buy_date=buy_date,items_information=price_data)
        form_title = request.form.get('title')
        form_store = request.form.get('store')
        form_natural_price = request.form.get('natural_price')
        form_num = request.form.get('num')
        form_buy_date = request.form.get('buy_date')
        form_sell_price = request.form.get('sell_price')

        product = Product(
            buy_date=form_buy_date,
            store=form_store,
            title=form_title,
            natural_price=form_natural_price,
            num=form_num,
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