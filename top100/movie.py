#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : movie.py
# @Author: Feng
# @Date  : 2019/9/13
# @Desc  :
import csv

import os
import requests
import re
from requests.exceptions import RequestException

import cProfile
import pstats

import lxml.html

etree = lxml.html.etree

from bs4 import BeautifulSoup
import json
import time


def get_one_page(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            return None
    except RequestException:
        return None


# 提取网页内容的方法 采取正则表达式
def parse_one_page(html):
    pattern = re.compile(
        '<dd>.*?board-index.*?>(\d+)</i>.*?<img data-src="(.*?)".*?name"><a.*?>(.*?)</a>.*?star">(.*?)</p>' \
        '.*?releasetime">(.*?)</p>.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>', re.S)
    items = re.findall(pattern, html)
    for item in items:
        yield {
            'index': item[0],
            'thumb': get_thumb(item[1]),
            'name': item[2],
            'star': item[3].strip()[3:],
            'time': get_release_time(item[4].strip()[5:]),
            'area': get_release_area(item[4].strip()[5:]),
            'score': item[5].strip() + item[6].strip()
        }


# # 采用lxml方法进行提取数据
# [0]：xpath后面添加了[0]是因为返回的是只有1个字符串的list，添加[0]是将list提取为字符串，使其简洁；
# Network：要在最原始的Network选项卡中定位，而不是Elements中，不然提取不到相关内容；
# class属性：p[@class = “star”]/text()表示提取class属性为”star”的p节点的文本值；
# 提取属性值：img[2]/@data-src’：提取img节点的data-src属性值，属性值后面无需添加’/text()’
def parse_one_page1(html):
    parse = etree.HTML(html)
    items = parse.xpath('//*[@id="app"]//div//dd')
    # xpath://*[@id="app"]/div/div/div[1]/dl/dd[1]
    for item in items:
        yield {
            'index': item.xpath('./i/text()')[0],
            'thumb': get_thumb(str(item.xpath('./a/img[2]/@data-src')[0].strip())),
            'name': item.xpath('./a/@title')[0],
            'star': item.xpath('.//p[@class = "star"]/text()')[0].strip(),
            'time': get_release_time(item.xpath('.//p[@class = "releasetime"]/text()')[0].strip()[5:]),
            'area': get_release_area(item.xpath('.//p[@class = "releasetime"]/text()')[0].strip()[5:]),
            'score': item.xpath('.//p[@class = "score"]/i[1]/text()')[0] +
                     item.xpath('.//p[@class = "score"]/i[2]/text()')[0]
        }


# beautiful soup + css选择器
def parse_one_page2(html):
    soup = BeautifulSoup(html, 'lxml')
    items = range(10)
    for item in items:
        yield {
            'index': soup.select('dd i.board-index')[item].string,
            'thumb': get_thumb(soup.select('a > img.board-img')[item]['data-src']),
            'name': soup.select('.name a')[item].string,
            'star': soup.select('.star')[item].string.strip()[3:],
            'time': get_release_time(soup.select('.releasetime')[item].string.strip()[5:]),
            'area': get_release_area(soup.select('.releasetime')[item].string.strip()[5:]),
            'score': soup.select('.integer')[item].string + soup.select('.fraction')[item].string
        }


# beautiful soup + find_all函数
def parse_one_page3(html):
    soup = BeautifulSoup(html, 'lxml')
    items = range(10)
    for item in items:
        yield {
            'index': soup.find_all(class_='board-index')[item].string,
            'thumb': soup.find_all(class_='board-img')[item].attrs['data-src'],
            'name': soup.find_all(name='p', attrs={'class': 'name'})[item].string,
            'star': soup.find_all(name='p', attrs={'class': 'star'})[item].string.strip()[3:],
            'time': get_release_time(soup.find_all(class_='releasetime')[item].string.strip()[5:]),
            'area': get_release_area(soup.find_all(class_='releasetime')[item].string.strip()[5:]),
            'score': soup.find_all(name='i', attrs={'class': 'integer'})[item].string.strip() +
                     soup.find_all(name='i', attrs={'class': 'fraction'})[item].string.strip()
        }


# re.S:匹配任意字符，如果不加，则无法匹配换行符；
# yield:使用yield的好处是作为生成器，可以遍历迭代，并且将数据整理形成字典，输出结果美观。具体用法可参考：https://blog.csdn.net/zhangpinghao/article/details/18716275；
# .strip():用于去掉字符串中的空格。

# 提取图片
def get_thumb(url):
    pattern = re.compile(r'(.*?)@.*?')
    thumb = re.search(pattern, url)
    return thumb.group(1)


# ‘r’：正则前面加上’r’ 是为了告诉编译器这个string是个raw string，不要转意’\’。当一个字符串使用了正则表达式后，最好在前面加上’r’；
# ‘|’ ‘$’： 正则’|’表示或’，’$’表示匹配一行字符串的结尾；
# .group(1)：意思是返回search匹配的第一个括号中的结果，即(.*?)，gropup()则返回所有结果2013-12-18(，group(1)返回’（’。

# 提取上映时间
def get_release_time(data):
    pattern = re.compile(r'(.*?)(\(|$)')
    items = re.search(pattern, data)
    if items is None:
        return "None"
    return items.group(1)


def get_release_area(data):
    pattern = re.compile(r'.*\((.*?)\)')
    items = re.search(pattern, data)
    if items is None:
        return None
    return items.group(1)


# 数据的存储
def write_to_file(item,dir_path):
    with open(dir_path + '猫眼top100.csv', 'a', encoding='utf_8_sig', newline='') as f:
        fieldnames = ['index', 'thumb', 'name', 'star', 'time', 'area', 'score']
        w = csv.DictWriter(f, fieldnames=fieldnames)
        # w.writeheader()
        w.writerow(item)


def download_thumb(name, url, num,dir_path):
    try:
        response = requests.get(url)
        with open(dir_path + name + '.jpg', 'wb') as f:
            f.write(response.content)
            print('第%s部电影封面下载完毕' % num)
            print('---------------------------')

    except RequestException as e:
        print(e)


def main(offset):
    url = "https://maoyan.com/board/4?offset={0}".format(offset)
    html = get_one_page(url)
    dir_path_data = './top100/data/'

    if not os.path.exists(dir_path_data):
        os.makedirs(dir_path_data)

    dir_path_photo = './top100/picture/'
    if not os.path.exists(dir_path_photo):
        os.makedirs(dir_path_photo)

    for item in parse_one_page(html):
    # for item in parse_one_page1(html):
    # for item in parse_one_page2(html):
    # for item in parse_one_page3(html):
        write_to_file(item,dir_path_data)
        download_thumb(item['name'], item['thumb'], item['index'],dir_path_photo)


def run1():
    for i in range(10):
        number = i * 10
        main(number)


# 单线程启动
# if __name__ == '__main__':
#     run1()

def run2():
    pool = Pool()
    pool.map(main, [i * 10 for i in range(10)])


# 多进程启动
from multiprocessing import Pool

if __name__ == '__main__':
    log_path = "./top100/"
    if not os.path.exists(log_path):
        os.makedirs(log_path)
    else:
        log_file = log_path + 'log'
        with open(log_file, "w", encoding='utf-8') as f:
            pass

        cProfile.run('run2()', log_file)

        p = pstats.Stats(log_file)
        p.strip_dirs().sort_stats("cumulative").print_stats(200)
