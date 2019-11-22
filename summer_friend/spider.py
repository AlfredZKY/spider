import requests
import os
from tqdm import tqdm

import asyncio
import aiohttp

# param1:传入的url
# param2:保存文件的路径


def download_from_url(url, dst):
    response = requests.get(url, stream=True)
    file_size = int(response.headers['content-length'])

    if os.path.exists(dst):
        first_byte = os.path.getsize(dst)
    else:
        first_byte = 0

    if first_byte >= file_size:
        return file_size

    header = {"Range": f"bytes={first_byte} - {file_size}"}

    pbar = tqdm(
        total=file_size, initial=first_byte, unit='B', unit_scale=True, desc=dst
    )

    req = requests.get(url,headers=header,stream=True)

    with (open(dst,"ab")) as f:
        for chunk in req.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                pbar.update(1024)
    pbar.close()
    return file_size


if __name__ == "__main__":
    url = ""
    download_from_url(url, "夏目友人帐第一集.mp4")
