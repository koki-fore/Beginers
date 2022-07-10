from datetime import datetime
import locale
from pathlib import Path
import re

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
########################################################

test_dir_path = u"./Beginers/result"
start = 0
end = 10

for it in Path(test_dir_path).glob("*"):
    with open(it,"r") as f:
        reader = f.read().split("\n")
        for i in range(start,end):
            now_result = parse_date_time(reader[i])
            if(now_result != False):
                print("{} : {}".format(reader[i],now_result))
