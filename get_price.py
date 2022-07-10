from pathlib import Path
import re

from pandas import to_numeric

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

def get_price(price_str):
    easy_price = to_easy_price(price_str)
    price_format = ["\\"]
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

test_dir_path = u"../Beginners/Beginers/result"
start = 0
end = 15

for it in Path(test_dir_path).glob("*"):
    with open(it,"r") as f:
        reader = f.read().split("\n")
        for i in range(start,end):
            now_result = get_price(reader[i])
            if(now_result != False):
                print("{}, {}".format(reader[i],now_result))
