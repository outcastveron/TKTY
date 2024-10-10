import time
import os
import re
import base64
import datetime
import requests
import threading
from queue import Queue
from datetime import datetime


#  获取远程体育直播源文件
url = "https://mirror.ghproxy.com/https://raw.githubusercontent.com/xingzhe010203/xingzhe/main/TKTY.m3u"
response = requests.get(url)
m3u_content = response.text

# 移除第一行
# m3u_content = m3u_content.split('\n', 1)[1]

# 初始化变量
group_name = ""
channel_name = ""
channel_link = ""
output_dict = {}

# 处理每两行为一组的情况
for line in m3u_content.split('\n'):
    if line.startswith("#EXTINF"):
        #  获取分组和频道
if 'group-title="' in line:
    group_name = line.split('group-title="')[1].split('"')[0]
    channel_name = line.split(',')[-1]
else:
    group_name = None
    channel_name = None
elif line.startswith("http"):
        # 获取频道链接
        channel_link = line
        # 合并频道名和频道链接
        combined_link = f"{channel_name},{channel_link}"

        # 将组名作为键，合并链接作为值存储在字典中
        if group_name not in output_dict:
            output_dict[group_name] = []
        output_dict[group_name].append(combined_link)

# 将结果写入 sport.txt 文件
with open("sport.txt", "w", encoding="utf-8") as output_file:
    # 遍历字典，写入结果文件
    for group_name, links in output_dict.items():
        output_file.write(f"{group_name},#genre#\n")
        for link in links:
            output_file.write(f"{link}\n")
            
with open("sport.txt", "a", encoding="utf-8") as output:  # 使用 "a" 模式以追加方式打开文件
    now = datetime.now()  # 这一行的缩进应与上一行的 with 语句对齐
    output.write(f"更新时间,#genre#\n")
    output.write(f"{now.strftime('%Y-%m-%d')},url\n")
    output.write(f"{now.strftime('%H:%M:%S')},url\n")

def txt_to_m3u(input_file, output_file):
    # 读取txt文件内容
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # 打开m3u文件并写入内容
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('#EXTM3U\n')

        # 初始化genre变量
        genre = ''

        # 遍历txt文件内容
        for line in lines:
            line = line.strip()
            if "," in line:  # 防止文件里面缺失“,”号报错
                # if line:
                # 检查是否是genre行
                channel_name, channel_url = line.split(',', 1)
                if channel_url == '#genre#':
                    genre = channel_name
                    print(genre)
                else:
                    # 将频道信息写入m3u文件
                    f.write(f'#EXTINF:-1 group-title="{genre}",{channel_name}\n')
                    f.write(f'{channel_url}\n')


# 将txt文件转换为m3u文件
txt_to_m3u('sport.txt', 'sport.m3u')

print("任务运行完毕，分类频道列表可查看文件夹内sport.txt和sport.m3u文件！")
