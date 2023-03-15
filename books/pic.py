import requests
from bs4 import BeautifulSoup
import re
import os
import csv
import time
import io
import random


game_list_file = "./lastaddgames.csv"
folder_path = "./temp"

if not os.path.exists(folder_path):
    os.mkdir(folder_path)

# 清空temp文件夹内的所有文件
for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)
    try:
        if os.path.isfile(file_path):
            os.unlink(file_path)
    except Exception as e:
        print(f"Failed to delete {file_path}. Reason: {e}")

def download_cover_image(game_name):
    # 设置搜索页面的URL和请求头
    url = f"https://m.douban.com/search/?query={game_name}&type=3114"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.69'
    }

    # 发送请求，获取搜索页面的HTML代码
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')

    # 将HTML代码写入文件，方便调试
    # with open(f'{folder_path}/{game_name}_find.html', 'w', encoding='utf-8') as f:
    #     f.write(soup.prettify())

    # 查找所有搜索结果中游戏的标题和封面图片URL
    game_links = soup.find_all('span', {'class': 'subject-title'})
    if not game_links:
        print(f"No game found with the name: {game_name}")
        return

    # 遍历每个游戏的标题、封面图片URL和链接
    for game_link in game_links:
        # 提取游戏标题、封面图片URL、链接和游戏ID
        game_title = game_link.text.strip()
        img_url = game_link.find_previous('img')['src']
        game_link_url = game_link.find_parent('a')['href']
        game_id = re.findall(r'/(\d+)/$', game_link_url.replace('/game/subject/', '/game/'))[0]

        # 替换掉标题中的特殊字符，方便保存为文件名
        game_title2 = re.sub(r'[^\w]+', '_', game_title)

        # 使用curl命令下载封面图片
        cmd = f"curl -sSL {img_url} -o {folder_path}/{game_name}_{game_title2}.jpg"
        result = os.system(cmd)

        # 根据下载结果输出相应信息
        if result == 0:
            print(f"成功下载《{game_title}》的封面图片！")
        else:
            print(f"下载《{game_title}》的封面图片失败！")

        # 构造游戏链接
        game_url = f"https://www.douban.com/game/{game_id}/"

        # 输出游戏标题、封面图片URL和链接
        print(f"游戏标题：{game_title}")
        print(f"封面图片URL：{img_url}")
        print(f"游戏链接：{game_url}")

        # 根据下载结果输出相应信息
        if result == 0:
            print(f"成功下载《{game_title}》的封面图片！")
        else:
            print(f"下载《{game_title}》的封面图片失败！")

    # 构造游戏链接
    game_url = f"https://www.douban.com/game/{game_id}/"

    # 输出游戏标题、封面图片URL和
    # 构造游戏链接
    game_url = f"https://www.douban.com/game/{game_id}/"

    # 输出游戏标题、封面图片URL和链接
    print(f"游戏标题：{game_title}")
    print(f"封面图片URL：{img_url}")
    print(f"游戏链接：{game_url}")
    print()





# 读取游戏名称列表
with open(game_list_file, 'r', newline='') as csvfile:
    csvreader = csv.reader(csvfile)
    next(csvreader)  # 跳过标题行
    for row in csvreader:
        game_name = row[0]
        download_cover_image(game_name)
        time.sleep(random.uniform(3, 5))



