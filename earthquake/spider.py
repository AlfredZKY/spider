import os
import requests
import chardet
import json
import csv

from os import path
from requests import RequestException

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'
}

# 获取当前文件路径
d = path.dirname(__file__) if "__file__" in locals() else os.getcwd()

def get_one_page(url):
    try:
        response = requests.get(url,headers=headers)
        if response.status_code == 200:
            # 获取编码信息
            encoding = chardet.detect(response.content)['encoding']
            # print(encoding)
            html = response.content.decode(encoding)
            return html
        else:
            print("spider fail")
            return None
    except RequestException:
        print("spider failed")

def parse_one_page(html):
    html = html["shuju"]
    for item in html:
        yield{
            'CATA_ID' : item["CATA_ID"],
            '震级(M)':item["M"],
            '发震时刻(UTC+8)':item["O_TIME"],
            '维度(°)':item["EPI_LAT"],
            '经度(°)':item["EPI_LON"],
            '深度(千米)':item["EPI_DEPTH"],
            '参考位置':item["LOCATION_C"],
            '具体链接':f'http://news.ceic.ac.cn/{item["CATA_ID"]}.html'
        }

def save_to_csv(item):
    with open(path.join(d+'/data/最近一年世界地震情况.csv'),'a',encoding='utf_8_sig',newline='') as f:
        # a 为追加模式 utf_8_sig格式导出csv不乱码
        filename = ['CATA_ID','震级(M)','发震时刻(UTC+8)','维度(°)','经度(°)','深度(千米)','参考位置','具体链接']
        writer = csv.DictWriter(f,fieldnames=filename)
        writer.writerow(item)

def main(page):
    print(page)
    url = "http://www.ceic.ac.cn/ajax/speedsearch?num=6&&page={0}".format(page)
    print(url)
    html = get_one_page(url)[1:-1]
    # print(type(html))
    html = json.loads(html)
    for item in parse_one_page(html):
        save_to_csv(item)



if __name__ == "__main__":
    for page in range(1,58):
        main(page)