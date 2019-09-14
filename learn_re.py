#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : learn_re.py
# @Author: Feng
# @Date  : 2019/9/13
# @Desc  :

import re

result = re.match("hello", "hello.cn")
print(result.group())

# 匹配单个字符
ret = re.match(".", "M")
print(ret.group())

ret = re.match("t.o", "too")
print(ret.group())

ret = re.match("t.o", "two")
print(ret.group())

print("------------------------------------")
# 匹配 []
# 如果hello的首字符小写，那么正则表达式需要小写的h
ret = re.match("h", "hello python")
print(ret.group())

# 如果hello的首字符大写，那么正则表达式需要小写的H
ret = re.match("[hH]", "Hello Python")
print(ret.group())

# 大小写h都可以的情况
ret = re.match("[hH]", "hello Python")
print(ret.group())

ret = re.match("[hH]", "Hello Python")
print(ret.group())

ret = re.match("[hH]ello Python", "Hello Python")
print(ret.group())

# 匹配0-9第一种写法
ret = re.match("[0123456789]Hello Python", "7Hello Python")
print(ret.group())

# 匹配0-9第二种写法
ret = re.match("[0-9]Hello Python", "7Hello Python")
print(ret.group())

# 下面这个正则不能够匹配到数字4，因此ret为None
ret = re.match("[0-35-9]Hello Python", "4Hello Python")
# print(ret.group())
