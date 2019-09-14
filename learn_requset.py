#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : learn_re.py
# @Author: Feng
# @Date  : 2019/9/13
# @Desc  :

import requests

url = "http://www.baidu.com"

# 定义自定义请求头
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) \
    Chrome/72.0.3626.121 Safari/537.36"
}

# 定义GET请求参数
params = {
    "kw": "hello"
}

# 使用 GET 请求参数发送请求
response = requests.get(url, headers=headers, params=params)

# 使用 POST 请求参数发送请求
response = requests.post(url, headers=headers, params=params)

# response 常用属性
# response.text 返回响应内容，响应内容为str类型
# response.content 返回响应内容，响应内容为类型
# response.status_code 返回响应状态码
# response.request.headers 返回请求头
# response.header 返回响应头
# response.cookies 返回响应的RequestsCookieJar对象

# 获取文本内容
html = response.text
print(html)

# 获取字节数据
content = response.content
# 转换成字符串类型
html = content.decode('utf-8')
print(html)

# response.cookies操作

# 返回RequestsCookieJar 对象
cookies = response.cookies
# RequestsCookieJar转dict
cookie_dict = requests.utils.dict_from_cookiejar(cookies)

# dict 转 RequestsCookieJarre
requests.utils.cookiejar_from_dict(cookie_dict)

# 对cookie进行操作，把一个字典添加到cookiejar中
# requests.utils.add_dict_to_cookiejar()

# 保存图片
url = "http://docs.python-requests.org/zh_CN/latest/_static/requests-sidebar.png"
response = requests.get(url)
with open("image.png", "wb") as f:
    f.write(response.content)
