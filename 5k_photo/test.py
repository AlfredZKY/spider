import requests

url = 'https://images.unsplash.com/photo-1529770358086-0eae9de0905f'

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
}
if __name__ == '__main__':
    response = requests.get(url, headers=headers)
    print(int(response.headers['content-length']))
    if response.status_code == 200:
        print("ok")
        # with open('test.jpg','wb') as f:
        #     f.write(response.content)
    else:
        print("failed")
