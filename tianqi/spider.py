import requests
import re
import os
import csv
import pandas as pd
import time
import random

from requests.exceptions import RequestException

dir_path_data = './tianqi/data/'
if not os.path.exists(dir_path_data):
    os.makedirs(dir_path_data)

urls = []
info = []

# 数据的存储
def write_to_file():
    # 生成数据表
    weather = pd.concat(info)
    # 数据导出
    weather.to_csv(dir_path_data + 'weather.csv',index = False)

def parse_all_page():
    for url in urls:
        seconds = random.randint(3,6)
        try:
            response = requests.get(url)
            if response.status_code == 200:
                response = response.text
                # 正则匹配
                ymd = re.findall("ymd:'(.*?)',",response)
                high = re.findall("bWendu:'(.*?)℃',",response)
                low = re.findall("yWendu:'(.*?)℃',",response)
                tianqi = re.findall("tianqi:'(.*?)',",response)
                fengxiang = re.findall("fengxiang:'(.*?)',",response)
                fengli = re.findall(",fengli:'(.*?)'",response)
                aqi = re.findall("aqi:'(.*?)',",response)
                aqiInfo = re.findall("aqiInfo:'(.*?)',",response)
                aqiLevel = re.findall(",aqiLevel:'(.*?)'",response)
        except RequestException:
            print("spider failed")

        if len(aqi) == 0:
            aqi = None
            aqiInfo = None
            aqiLevel = None
            info.append(pd.DataFrame({'ymd':ymd,'high':high,'low':low,'tianqi':tianqi,'fengxiang':fengxiang,'fengli':fengli,'aqi':aqi,'aqiInfo':aqiInfo,'aqiLevel':aqiLevel}))
        else:
            info.append(pd.DataFrame({'ymd':ymd,'high':high,'low':low,'tianqi':tianqi,'fengxiang':fengxiang,'fengli':fengli,'aqi':aqi,'aqiInfo':aqiInfo,'aqiLevel':aqiLevel}))
    time.sleep(seconds)

def get_all_page():
    for year in range(2011,2019):
        for month in range(1,13):
            if year <= 2016:
                urls.append('http://tianqi.2345.com/t/wea_history/js/58362_%s%s.js' %(year,month))
            else:
                if month < 10:
                    urls.append('http://tianqi.2345.com/t/wea_history/js/%s0%s/58362_%s0%s.js' %(year,month,year,month))
                else:
                    urls.append('http://tianqi.2345.com/t/wea_history/js/%s%s/58362_%s%s.js' %(year,month,year,month))

def main():
    get_all_page()
    parse_all_page()
    write_to_file()
    print(urls)

if __name__ == '__main__':
    main()