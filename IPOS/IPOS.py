import pandas as pd
import csv
import os
import requests
import lxml.html
etree = lxml.html.etree

from bs4 import BeautifulSoup
from requests.exceptions import RequestException
from urllib.parse import urlencode

dir_path_data = './IPOS/data/'
if not os.path.exists(dir_path_data):
    os.makedirs(dir_path_data)

# ## 爬取中商情报网上的上市公司
# name = list(["序号","股票代码","股票简称","公司名称","省份","城市","主营业务收入(201712)","净利润(201712)","员工人数","上市日期","招股书","公司财报","行业分类","产品类型","主营业务"])
# for i in range(1,4):
#     url = 'http://s.askci.com/stock/a/?reportTime=2018-12-31&pageNum=%s' % str(i)
#     tb = pd.read_html(url)[3] # 经观察发现所需表格是网页中第4个表格，故为[3]
#     tb.to_csv( dir_path_data + r'2.csv',mode='a',encoding='utf-8_sig',header=name,index=0)
#     print('第' + str(i) + '页抓取完成')

# 网页提取
def get_one_page(i):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'
        }

        params = {
            'reportTime':'2018-12-31', # 查询时间
            'pageNum' : i   # 查询页面数
        }

        url = 'http://s.askci.com/stock/a/?' + urlencode(params)
        response = requests.get(url,headers=headers)

        if response.status_code == 200:
            return response.text
    except RequestException:
        print("spider failed")

# 解析网页数据
def parse_one_page(html):
    soup = BeautifulSoup(html,'lxml')
    # css 选择器 选择id select('#link1')
    content = soup.select("#myTable04")[0]
    tbl = pd.read_html(content.prettify(),header = 0)[0]
    # prettify()优化代码,[0]从pd.read_html返回的list中提取出DataFrame
    tbl.rename(columns = {'序号':'serial_number', '股票代码':'stock_code', '股票简称':'stock_abbre', '公司名称':'company_name', '省份':'province', '城市':'city', '主营业务收入(201712)':'main_bussiness_income', '净利润(201712)':'net_profit', '员工人数':'employees', '上市日期':'listing_date', '招股书':'zhaogushu', '公司财报':'financial_report', '行业分类':'industry_classification', '产品类型':'industry_type', '主营业务':'main_business'},inplace = True)
    print(tbl)

def main(page):
    for i in range(1,page):
        html = get_one_page(i)
        parse_one_page(html)

if __name__ == '__main__':
    main(4)