import os  # 用于创建文件夹
import time  # 用于添加延时
import requests  # 用于发送HTTP请求
from lxml import etree  # 用于解析HTML文档

# 设置请求头信息
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
}

# 歌单页面的URL
url = 'https://music.163.com/playlist?id=108384918'

# 发送GET请求，获取歌单页面的HTML内容
response = requests.get(url, headers=headers)

# 使用lxml库对HTML内容进行解析
html = etree.HTML(response.text)

# 使用XPath表达式选取所有包含/song?的链接元素，这些元素对应歌曲的链接
music_label_list = html.xpath('//a[contains(@href,"/song?")]')

# 如果不存在名为music的文件夹，则创建文件夹
if not os.path.exists('music'):
    os.mkdir('music')

# 遍历歌曲链接元素列表
for music_label in music_label_list:
    # 获取歌曲链接的href属性值
    href = music_label.xpath('./@href')[0]
    # 从链接中提取歌曲ID
    music_id = href.split('=')[1]
    # 如果歌曲ID是数字，则继续处理
    if music_id.isdigit():
        print('ID数据：', music_id)
        # 获取歌曲名字
        music_name = music_label.xpath('./text()')[0]
        print('歌曲名字：', music_name)
        # 构造歌曲的下载链接
        music_url = 'http://music.163.com/song/media/outer/url?id=' + music_id
        # 发送GET请求，获取歌曲内容
        response = requests.get(music_url, headers=headers)
        # 将歌曲内容保存为以歌曲名字命名的MP3文件
        with open(f'./music/{music_name}.mp3', 'wb') as file:
            file.write(response.content)
        # 打印下载成功的提示信息
        print(f'《{music_name}》下载成功。。。。。。')
        # 添加1秒的延时，防止请求频率过快
        time.sleep(1)
