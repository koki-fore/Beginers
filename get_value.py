from datetime import datetime
import locale
from pathlib import Path
import re
from pandas import to_numeric

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
        date_value = "Please input datetime!"
    return date_value,price_answer


test_dir_path = u"../Beginners/Beginers/result"
start = 0
end = 10

for it in Path(test_dir_path).glob("*"):
    print("\n{}".format(it))
    with open(it,"r") as f:
        reader = f.read().split("\n")
        date_value, price_data = Get_all_value(reader)
        print(date_value)
        for now_price in price_data:
            print(now_price)

# test = ["2020年5月10日 14時00分","2020510 14:00","2020/5/10 14:00","2020-5-10 14:00"]
# test = ["2020年5月10日 (土)14時00分","2020510 (Sat)14:00"]
