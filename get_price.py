from pathlib import Path
import re
from numpy import triu

from pandas import to_numeric


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
def get_all_value(data):
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

def get_true_all_value(answer_data):
    res = []
    for now in answer_data:
        if(now[1] == -1):
            continue
        res.append(now)
    return res

test_dir_path = u"../Beginners/Beginers/result"


for it in Path(test_dir_path).glob("*"):
    print("\n{}".format(it))
    with open(it,"r") as f:
        reader = f.read().split("\n")
        answer = get_all_value(reader)
        true_answer = get_true_all_value(answer)
        for it in true_answer:
            print(it)