import requests
import os
import re

import lxml.html
etree = lxml.html.etree

from bs4 import BeautifulSoup
from requests.exceptions import RequestException


data_path = './PHOTO_wangyi/data/'


def get_one_page():
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'
        }

        url = 'http://data.163.com/18/0901/01/DQJ3D0D9000181IU.html'
        response = requests.get(url,headers=headers)
        if response.status_code == 200:
            #print(response.text)
            return response.text
        else:
            print("spider failed")
    except RequestException:
        print("spider failed")

def parse_data_re():
    html = get_one_page()
    pattern = re.compile('<p>.*?<img alt="房租".*?src="(.*?)".*?style',re.S)
    items = re.findall(pattern,html)
    # print(items)
    for item in items:
        yield{
            'urls':item
        }

def parse_data_Xpath():
    html = get_one_page()
    parse = etree.HTML(html)
    items = parse.xpath('*//p//img[@alt = "房租"]/@src')
    for item in items:
        yield{
            'urls':item
        }

def parse_data_Css():
    html = get_one_page()
    soup = BeautifulSoup(html,'lxml')
    items = soup.select('p>a>img') # > 表示下级节点
    for item in items:
        yield{
            'urls':item['src']
        }

def parse_data_find_all():
    html = get_one_page()
    soup = BeautifulSoup(html,'lxml')

    # 获取title
    title = soup.h1.string # 每个网页只能拥有一个<H1>标签,因此唯一

    item = soup.find_all(name='img',width=['100%'])
    for i in range(len(item)):
        pic = item[i].attrs['src']
        yield{
            'title':title,
            'pic':pic,
            'num':i
        }

def save_pic(pic):
    title = pic.get('title')
    url = pic.get('pic')

    # 设置图片编号顺序
    num = pic.get('num')
    new_data = data_path + title + str(num) + '/'
    if not os.path.exists(new_data):
        os.makedirs(new_data)

    # 获取url图片网页信息
    headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'
        }
    response = requests.get(url,headers=headers)
    try:
        if response.status_code == 200:
            file_path = new_data + '{0}{1}.{2}'.format(title,num,'jpg')
            print(file_path)
            if not os.path.exists(file_path):
                # 下载图片
                with open(file_path ,'wb') as f:
                    f.write(response.content)
                    print('该图片已下载完成',title)
            else:
                print('该图片{0}已下载完成'.format(title))
    except RequestException as e:
        print(e,'图片获取失败')
        return None
#     f.write(response.content)
# 从外到内定位url的位置：<p>节点-<a>节点-<img>节点里的src属性值

def main():
    # for item in parse_data_re():
    #     print(item)
    # for item in parse_data_Xpath():
    #     print(item)
    # for item in parse_data_Css():
    #     print(item)
    for item in parse_data_find_all():
        save_pic(item)

if __name__ == '__main__':
    main()