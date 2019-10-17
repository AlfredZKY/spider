import requests
import pandas as pd
import random
import time
import re
import operator as op
import os

from bs4 import BeautifulSoup
from requests.exceptions import RequestException

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'
}

dir_path_data = './world_student/data/'

def get_country(html):
    soup = BeautifulSoup(html,'lxml')
    countries = soup.select('td > a > img')
    lst = []
    for i in countries:
        src = i.get("src")
        pattern = re.compile(r"flag.*\/(.*?).png")
        country = re.findall(pattern,src)[0]
        lst.append(country)
    return lst

def parse_one_page(html,i):
    tb = pd.read_html(html)[0]

    # 重命名表格列，不需要的列用数字表示
    tb.columns = ['world rank','university',2,3,'score',5]

    # 删除后面不需要的评分列
    tb.drop([2,3,5],axis=1,inplace=True)

    # 重新建立索引，100以后的是区间，需要重新构建索引
    tb['index_rank'] = tb.index
    tb['index_rank'] = tb['index_rank'].astype(int) + 1

    # 增加一列年份
    tb['year'] = i
    tb['country'] = get_country(html)
    return tb

def get_one_page(year):
    try:
        url = 'http://www.zuihaodaxue.com/ARWU{0}.html'.format(str(year))
        response = requests.get(url,headers=headers)
        html = response.content
        # html = response.text.encode('iso-8859-1').decode('gbk')

        if response.status_code == 200:
            # return response.text
            print(response.apparent_encoding)
            return html
        else:
            print("spider Failed")
            return None
    except RequestException:
        print("spider Failed")
        return None

def main(year):
    for i in range(2009,year):
        seconds = random.randint(1,6)
        html = get_one_page(i)
        tb = parse_one_page(html,i)
        save_csv(tb)
        time.sleep(seconds)
        print(i,'年排名提取完成')
        analysis()

def save_csv(tb):
    tb.to_csv(dir_path_data + r'university.csv',mode='a',encoding='utf-8_sig',header=True,index=0)

def analysis():
    df = pd.read_csv(dir_path_data + r'university.csv')

    # 只包括内地
    df = df.query("(country == 'China')")
    df['index_rank_score'] = df['index_rank']
    df['index_rank'] = df['index_rank'].astype(int)

    def topn(df):
        top = df.sort_values(['year','index_rank'],ascending = True)
        return top[:20].reset_index()

    df = df.groupby(by=['year']).apply(topn)

    # 更改列顺序
    df =df[['university','index_rank_score','index_rank','year']]

    # 重命名列
    df.rename(columns={
        'university':'name',
        'index_rank_score':'type',
        'index_rank':'value',
        'year':'date'},inplace=True)
    # 输出结果
    df.to_csv(dir_path_data + r'university_ranking.csv',mode='w',encoding='utf-8_sig',header=True,index=False)

if __name__ == '__main__':
    if not os.path.exists(dir_path_data):
        os.makedirs(dir_path_data)
    main(2019)