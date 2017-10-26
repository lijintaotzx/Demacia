# coding=utf-8
import re


# 正则匹配电话号码
def check_phone_num(phone):
    p2 = re.compile('^0\d{2,3}\d{7,8}$|^1[358]\d{9}$|^147\d{8}')
    phonematch = p2.match(phone)
    if phonematch:
        return True
    else:
        return False