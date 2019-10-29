import time
import requests
import os
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'
}

dir_path_data = './air_quality/data/'
if not os.path.exists(dir_path_data):
    os.makedirs(dir_path_data)

for i in range(1, 13):
    time.sleep(5)
    url = 'http://www.tianqihoubao.com/aqi/tianjin-2017' + \
        str("%02d" % i) + '.html'
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    tr = soup.find_all('tr')
    # print(tr)
    # 去除标签栏
    for j in tr[1:]:
        td = j.find_all('td')
        Date = td[0].get_text().strip()
        Qurity_grade = td[1].get_text().strip()
        AQI = td[2].get_text().strip()
        AQI_rank = td[3].get_text().strip()
        PM = td[4].get_text().strip()
        with open(dir_path_data + 'air_tianjin_2017.csv', 'a+', encoding='utf-8-sig') as f:
            f.write(Date + ',' + Qurity_grade + ',' +
                    AQI + ',' + AQI_rank + ',' + PM + '\n')
