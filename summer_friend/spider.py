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
    url = "http://v11-tt.ixigua.com/7da2b219bc734de0f0d04706a9629b61/5c77ed4b/video/m/220d4f4e99b7bfd49efb110892d892bea9011612eb3100006b7bebf69d81/?rc=am12NDw4dGlqajMzNzYzM0ApQHRAbzU6Ojw8MzQzMzU4NTUzNDVvQGgzdSlAZjN1KWRzcmd5a3VyZ3lybHh3Zjc2QHFubHBfZDJrbV8tLTYxL3NzLW8jbyMxLTEtLzEtLjMvLTUvNi06I28jOmEtcSM6YHZpXGJmK2BeYmYrXnFsOiMzLl4%3D"
    download_from_url(url, "夏目友人帐第一集.mp4")
