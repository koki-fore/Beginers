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

def get_price(price_str):
    easy_price = to_easy_price(price_str)
    price_format = ["\\"]
    for now in easy_price:
        for format in price_format:
            now_format = format
            if(is_price(now,now_format) == True):
                nums = re.findall(r'\d+',now)
                res = 0
                for i in nums:
                    res *= 1000
                    res += to_numeric(i)
                return res
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
