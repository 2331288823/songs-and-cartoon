import requests  # 用于解析HTML文档
import parsel  # 用于发送HTTP请求
import os  # 用于创建文件夹

# 目标漫画页面的URL
url = 'https://www.mkzhan.com/211471/'

# 请求头信息，包括Cookie、Referer、Host和User-Agent
headers = {
    'Cookie': '__login_his_sync=0; redirect_url=%2F207622%2F; UM_distinctid=18929cac20955b-0ed238a4d7fd63-7e56547f-1fa400-18929cac20ac70; CNZZDATA1261814609=1457200997-1688620024-%7C1688620024; CNZZDATA1262045698=972920694-1688623264-%7C1688623264; tourist_expires=1; cn_1262045698_dplus=%7B%22distinct_id%22%3A%20%2218929cac20955b-0ed238a4d7fd63-7e56547f-1fa400-18929cac20ac70%22%2C%22%24_sessionid%22%3A%200%2C%22%24_sessionTime%22%3A%201688623310%2C%22%24dp%22%3A%200%2C%22%24_sessionPVTime%22%3A%201688623310%7D',
    'referer': 'https://www.mkzhan.com/category/?is_vip=1',
    'host': 'www.mkzhan.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.67',
}

# 发送GET请求，获取漫画页面的HTML内容
resp = requests.get(url, headers=headers)

# 使用parsel库对HTML内容进行解析
selector = parsel.Selector(resp.text)

# 获取章节列表
li_list = selector.css('.chapter__list-box li')

# 遍历章节列表（倒序）
for li in list(reversed(li_list[2:])):
    # 获取章节ID和标题
    img_id = li.css('a::attr(data-chapterid)').get()
    title = li.css('a::text').get().strip()

    # 如果标题为空，则获取第二个文本节点作为标题
    if not title:
        title = li.css('a::text').getall()[1].strip()

    # 创建文件夹，以标题命名
    file_name = f'{title}\\'
    if not os.path.exists(file_name):
        os.mkdir(file_name)

    # 构造请求参数
    index_url = 'https://comic.mkzcdn.com/chapter/content/v1/'
    data = {
        'chapter_id': img_id,
        'comic_id': '211471',
        'format': '1',
        'quality': '1',
        'type': '1',
    }

    # 发送POST请求，获取漫画图片信息
    json_data = requests.get(index_url, params=data).json()
    imgs = json_data['data']['page']

    # 遍历图片信息列表
    page = 0
    for img in imgs:
        # 获取图片URL
        img_url = img['image']

        # 发送GET请求，获取图片内容
        img_content = requests.get(img_url).content

        # 打印标题和图片URL
        print(title, img_url)

        # 递增页数计数
        page += 1

        # 将图片内容保存到本地文件
        with open(file_name + str(page) + '.jpg', 'wb') as f:
            f.write(img_content)
