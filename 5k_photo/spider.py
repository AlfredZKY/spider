import requests
import os
import random
import time
import json
import sys
from contextlib import closing
from filetype import guess

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
}


def down_load(file_url, file_full_name, now_photo_count, all_photo_count):
    # 开始下载图片
    with closing(requests.get(file_url, headers=headers, stream=True)) as response:
        # 单次请求最大值
        chunk_size = 1024

        # 文件总大小
        content_size = int(response.headers['content-length'])

        # 当前已传输的大小
        data_count = 0

        with open(file_full_name, "wb") as file:
            for data in response.iter_content(chunk_size=chunk_size):
                print(file_url)
                file.write(data)
                done_block = int((data_count / content_size) * 50)
                data_count = data_count + len(data)
                now_jd = (data_count/content_size) * 100
                print("\r %s:[%s%s] %d%% %d/%d"
                      % (file_full_name, done_block * '♦', ' ' * (50-1-done_block), now_jd,
                         now_photo_count, all_photo_count), end=" ")

        # 下载完成后获取图片扩展片，并为其增加扩展名
        file_type = guess(file_full_name)
        os.rename(file_full_name, file_full_name + '.' + file_type.extension)

# 爬取不同类型图片


def crawler_photo(type_id, photo_count):
    # 最新1，最热2，女生3，星空4
    if(type_id == 1):
        url = 'https://service.paper.meiyuan.in/api/v2/columns/flow/5c68ffb9463b7fbfe72b0db0?page=1&per_page={0}'.format(
            photo_count)
    elif(type_id == 2):
        url = 'https://service.paper.meiyuan.in/api/v2/columns/flow/5c69251c9b1c011c41bb97be?page=1&per_page={0}'.format(
            photo_count)
    elif(type_id == 3):
        url = 'https://service.paper.meiyuan.in/api/v2/columns/flow/5c81087e6aee28c541eefc26?page=1&per_page={0}'.format(
            photo_count)
    elif(type_id == 4):
        url = 'https://service.paper.meiyuan.in/api/v2/columns/flow/5c81f64c96fad8fe211f5367?page=1&per_page={0}'.format(
            photo_count)

    # 获取图片链接列表，json格式
    response = requests.get(url, headers=headers)

    # 对json格式转化为python对象
    photo_data = json.loads(response.content)

    # 已经下载的图片张数
    now_photo = 1

    # 所有图片张数
    all_photo_count = len(photo_data)

    # 开始下载并保存5k分辨率壁纸
    for photo in photo_data:
        # 创建一个文件夹存放下载的图片(若已存在则不用重建)
        if not os.path.exists('./5k_photo/' + str(type_id)):
            os.makedirs('./5k_photo/' + str(type_id))

        # 准备下载的图片链接，5k超清壁纸链接
        file_url = photo['urls']['raw']

        # 准备下载的图片名称，不包好扩展名
        file_name_only = file_url.split('/')
        file_name_only = file_name_only[len(file_name_only)-1]

        # 准备保存到本地的完整路径
        file_full_name = './5k_photo/' + str(type_id) + '/' + file_name_only

        # 下载图片
        down_load(file_url, file_full_name, now_photo, all_photo_count)
        now_photo = now_photo + 1
        seconds = random.randint(2, 6)
        time.sleep(seconds)


if __name__ == '__main__':
    # 最新1，最热2，女生3，星空4
    wall_paper_id = 1
    wall_paper_count = 10
    while True:
        # 换行符
        print('\n\n')

        # 选择壁纸类型
        wall_paper_id = input(
            '壁纸类型：最新壁纸1，最热壁纸2，女生壁纸3，星空壁纸4\n请输入编号以便选择5K超清壁纸类型：')

        # 判断输入是否正确
        while(wall_paper_id != str(1) and wall_paper_id != str(2) and wall_paper_id != str(3) and wall_paper_id != str(4)):
            wall_paper_id = input(
                "壁纸类型：最新壁纸 1, 最热壁纸 2, 女生壁纸 3, 星空壁纸 4\n请输入编号以便选择5K超清壁纸类型：")
            if int(wall_paper_id) == 0:
                sys.exit(0)

        # 选择要下载的壁纸数量
        wall_paper_count = input("请输入要下载的5K超壁纸的数量:")

        while(int(wall_paper_count) <= 0):
            wall_paper_count = input("请输入要下载的5K超壁纸的数量:")

        # 开始爬取5k高清壁纸
        print("程序已经开始运行，请稍等......")
        crawler_photo(int(wall_paper_id), int(wall_paper_count))

        print('\n下载5K高清壁纸成功')
