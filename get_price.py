from pathlib import Path
import re

# Get price of item.
def to_easy_price(price_str):
    now = price_str.split(" ")
    next = [x for x in now if(x != '')]
    return next

def is_price(price_str,price_format):
    return price_str == price_format

def get_price(price_str):
    easy_price = to_easy_price(price_str)
    res = []
    for now in easy_price:
        result = re.findall(r"\d+",now)
        res.append(result)
    print("{}\n{}".format(price_str,res))


test_dir_path = u"./Beginers/result"
start = 0
end = 10

for it in Path(test_dir_path).glob("*"):
    print(it)
    with open(it,"r") as f:
        reader = f.read().split("\n")
        for i in range(start,end):
            now_result = get_price(reader[i])
            if(now_result == False):
                print(now_result)
