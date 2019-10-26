import requests
import random
import time
from urllib.parse import urlencode
import re
import os

from multiprocessing import Pool
from bs4 import BeautifulSoup
from hashlib import md5
from requests import RequestException


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'
}

# 解析索引界面网页内容
def parse_page_index(html):
    soup = BeautifulSoup(html,'lxml')

    # 获取每页文章数
    num =soup.find_all(name='div',class_='news_li')
    for i in range(len(num)):
        yield{
            # 获取title
            'title':soup.select('h2 a')[i].get_text(),
            # 获取图片url
            'url':'https://www.thepaper.cn/' + soup.select('h2 a')[i].attrs['href']
        }

# 获取索引界面内容
def get_page_index(i):
    try:
        paras = {
            'nodeids':25635,
            'pageidx':i
        }

        url = 'https://www.thepaper.cn/load_index.jsp?' + urlencode(paras)
        response = requests.get(url,headers=headers)
        if response.status_code == 200:
            # print(response.text)
            return response.text
    except RequestException:
        print("spider failed")
        return None

# 获取每条文章的详情页内容
def get_page_detail(item):
    url = item.get('url')
    try:
        response = requests.get(url,headers=headers)
        if response.status_code == 200:
            # print(response.text)
            return response.text
    except RequestException:
        print("spider failed")
        return None

# 解析每条文章的详情页内容
def parse_page_detail(html):
    soup = BeautifulSoup(html,'lxml')

    # 获取title 有的网页没有h1节点，因此必须要增加判断，否则会报错
    if soup.h1:
        # 因此网页只能拥有一个<h1>标签，因此唯一
        title = soup.h1.string

        # 有的图片节点用width='100%'表示，有的用600表示，因此用list表示
        items = soup.find_all(name='img',width=['100%','600'])
        for i in range(len(items)):
            pic = items[i].attrs['src']
            yield{
                'title':title,
                'pic':pic,
                'num':i
            }

def save_pic(pic):
    title = pic.get('title')
    # 标题规范命名:去掉符号和非法字符 | 等
    title = re.sub('[\/:*?"<>|]','-',title).strip()
    url = pic.get('pic')
    num = pic.get('num')

    dir_path_data = './ajax_pengpai/data/' + title + '/'
    if not os.path.exists(dir_path_data):
        os.makedirs(dir_path_data)

    # 获取图片存放地址
    try:
        response = requests.get(url,headers=headers)
        if response.status_code == 200:
            file_path = r'{0}{1}.{2}'.format(title,num,'jpg')
            file_path = dir_path_data + file_path
            # 文件名采用编号方便按顺序查看，而未采用哈希值md5(response.content).hexdigest()
            if not os.path.exists(file_path):
                # 开始下载图片
                with open(file_path,"wb") as f:
                    f.write(response.content)
                    print('文章"{0}"的第"{1}"张图片下载完成'.format(title,num))
            else:
                print('该图片{0}已下载'.format(title))
    except RequestException:
        print('spider failed')
        return None

def main(i):
    html = get_page_index(i)
    data = parse_page_index(html)
    for item in data:
        html = get_page_detail(item)
        data = parse_page_detail(html)
        for pic in data:
            save_pic(pic)
            time.sleep(random.randint(1,2))
        time.sleep(random.randint(2,6))

# 单进程
# if __name__ == '__main__':
#     for i in range(1,2):
#         main(i)
#         time.sleep(random.randint(2,6))

# 多线程
if __name__ == '__main__':
    pool = Pool()
    pool.map(main,[i for i in range(1,26)])





