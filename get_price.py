from pathlib import Path
import re

from pandas import to_numeric


########################################################
# Get price of item.
def to_easy_price(price_str):
    now = price_str.split(" ")
    next = [x for x in now if(x != '')]
    return next

def is_price(price_str,price_format):
    return price_str[:len(price_format)] == price_format

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

def create_price_format():
    pre_type = ["\\","*"]
    return pre_type

def get_price(price_str):
    easy_price = to_easy_price(price_str)
    price_format = create_price_format()
    item_name = ""
    cnt = 1
    for now in easy_price:
        for format in price_format:
            now_format = format
            if(is_price(now,now_format) == True):
                nums = re.findall(r'\d+',now)
                price = 0
                for i in nums:
                    price *= 1000
                    price += to_numeric(i)
                # 商品名，価格，個数
                return item_name,price,cnt 
        if(is_cnt(now) == True):
            cnt = re.find(r'\d+',now)
        else:
            item_name += now
    return False

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
            for pf in price_format:
                if(is_price(now_c,pf) == True):
                    price = re.findall(r'\d+',now_c)
                    if(len(price) > 0):
                        start = index
    return start,end


test_dir_path = u"../Beginners/Beginers/result"


for it in Path(test_dir_path).glob("*"):
    print("\n{}".format(it))
    with open(it,"r") as f:
        reader = f.read().split("\n")
        start,end = get_price_range(reader)
        print("{} to {}".format(start,end))
        for i in range(start,end):
            now_result = get_price(reader[i])
            if(now_result != False):
                print("{}, {}".format(reader[i],now_result))
