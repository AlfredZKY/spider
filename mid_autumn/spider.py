import requests
import time
import os
import random
import csv
import pandas as pd

from bs4 import BeautifulSoup


def get_data(name, city, code):
    print('正在下载城市%s的数据' % city)
    url = 'http://www.weather.com.cn/weather15d/%s.shtml' % code[2:]
    res = requests.get(url).content.decode()
    content = BeautifulSoup(res, 'html.parser')
    weather_list = content.find(
        'ul', attrs={'class': 't clearfix'}).find_all('li')
    items = map(parse_item, weather_list)
    # print(items)
    save_to_csv(name, city, items)
    seconds = random.randint(2, 7)
    time.sleep(seconds)


def save_to_csv(name, city, data):
    dir_path_weather = './mid_autumn/data/'
    if not os.path.exists(dir_path_weather):
        os.makedirs(dir_path_weather)
    # items = pd.DataFrame(data)
    # data = items.columns.tolist()
    # data.insert(0,'city')
    # for item in items:
    #     items['city'] = city
    # items.to_csv(dir_path_weather + '%s_data.csv' % name, header=None,index=False)
    if not os.path.exists(dir_path_weather + '%s_data.csv' % name):
        with open(dir_path_weather + '%s_data.csv' % name, 'a+', encoding='utf-8') as f:
            f.write('city,time,wea,tem,wind,wind_level\n')
            for d in data:
                try:
                    row = '{},{},{},{},{},{}\n'.format(city,
                                                       d['time'],
                                                       d['wea'],
                                                       d['tem'],
                                                       d['wind'],
                                                       d['wind_level'])
                    f.write(row)
                    # f.write('\n')
                except:
                    continue
    else:
        with open(dir_path_weather + '%s_data.csv' % name, 'a+', encoding='utf-8') as f:
            for d in data:
                try:
                    row = '{},{},{},{},{},{}\n'.format(city,
                                                       d['time'],
                                                       d['wea'],
                                                       d['tem'],
                                                       d['wind'],
                                                       d['wind_level'])
                    f.write(row)
                    # f.write('\n')
                except:
                    continue


def parse_item(item):
    time = item.find('span', attrs={'class': 'time'}).text
    wea = item.find('span', attrs={'class': 'wea'}).text
    tem = item.find('span', attrs={'class': 'tem'}).text
    wind = item.find('span', attrs={'class': 'wind'}).text
    wind_level = item.find('span', attrs={'class': 'wind1'}).text

    result = {
        'time': time,
        'wea': wea,
        'tem': tem,
        'wind': wind,
        'wind_level': wind_level
    }
    return result

# 准备数据阶段


def read_data():
    # 读取省份数据
    provincial = pd.read_csv('./mid_autumn/provincial_capital')
    china_city_code = pd.read_csv('./mid_autumn/china-city-list.csv')
    china_scenic_code = pd.read_csv(
        './mid_autumn/china-scenic-list.txt', sep='\t', encoding='utf-8')
    china_scenic_code.rename(columns={
        'ID': 'ID',
        ' 景点名称': 'name',
        '地区': 'area',
        '省/直辖市': 'provincial'}, inplace=True)
    # print(china_scenic_code.columns)
    # china_scenic_code.columns = ['ID','name','area','provincial']
    attraction = pd.read_csv('./mid_autumn/attractions')

    provincial_data = pd.DataFrame()
    attraction_data = pd.DataF

    # 抓取出省会数据
    # print(type(provincial['city'].values.tolist()))
    for i in provincial['city'].values.tolist():
        for j in china_city_code['City_CN'].values.tolist():
            if i == j:
                provincial_data = pd.concat(
                    [china_city_code[china_city_code['City_CN'] == j], provincial_data])

    for city in provincial_data['City_CN'].values.tolist():
        city_id = provincial_data[provincial_data['City_CN'] == city]['City_ID'].values.tolist()[
            0]
        get_data('weather', city, city_id)

    # 抓取出景点数据
    for a in attraction['attractions'].values.tolist():
        for c in china_scenic_code['name'].values.tolist():
            if c == a:
                attraction_data = pd.concat(
                    [china_scenic_code[china_scenic_code['name'] == c], attraction_data])

    for attrac in attraction_data['name'].values.tolist():
        city_id = attraction_data[attraction_data['name'] == attrac]['ID'].values.tolist()[
            0]
        get_data('attraction', attrac, city_id)


def main():
    read_data()


if __name__ == '__main__':
    main()
