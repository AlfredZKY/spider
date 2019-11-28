import requests
import json
from requests.exceptions import RequestException
import pymongo

client = pymongo.MongoClient('localhost',27017)
db = client.Huxiu
mongo_collection = db.huxiu_pyspider

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3941.4 Safari/537.36'
}

url = 'https://www-api.huxiu.com/v1/article/list?pagesize=22&recommend_time=1574920140'


def get_one_page(url=url):
    try:
        response = requests.get(url,headers=headers)
        if response.status_code == 200:
            res = json.loads(response.text)
            time = res.get('data').get('last_dateline')
            urls = 'https://www-api.huxiu.com/v1/article/list?pagesize=22&recommend_time={0}'.format(time)
            for item in res.get('data').get('dataList'):
                # data = [{
                #     'title':item.get('title'),
                #     'url':item.get('share_url'),
                #     'name':
                # }]
                print(item)
            get_one_page(urls)
    except RequestException:
        print('spider failed')

def main():
    get_one_page()


if __name__ == "__main__":
    main()