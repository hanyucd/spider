# -*- coding: UTF-8 -*-
import requests
import json
from bs4 import BeautifulSoup
import sys
reload(sys)
sys.setdefaultencoding('utf8') 

"""
QQ阅读爬虫，爬取每个网页每本小说的详情
start_URL = http://dushu.qq.com/store/index/sortkey/1/ps/30/p/1

"""
class QqRead:
    # 初始化， 传入基地址 和 参数
    def __init__(self, base_url):
        self.base_url = base_url

    ''' 传入页码， 获取该页需爬取的URL '''
    def getPage(self, pageNum):
        # 每个页面完整URL
        spider_url = self.base_url + str(pageNum)
        print '正在爬取的网页URL地址:', spider_url
        # 获取网页
        request = requests.get(spider_url)
        # 获取网页内容赋于变量
        html = request.text
        # 获取 BeautifulSoup对象
        soup = BeautifulSoup(html, 'html.parser')
        # 存储每页中需要爬取的链接，初始化空列表
        links = []
        # css选择器，通过组合查找
        for link in soup.select('div .bookImgBox'):
            # 获得页面 每本小说URL
             only_url = link.a.get('href')
             links.append(only_url)
        length = len(links)
        print '本页面共需爬取', length, '个URL.'
        # 返回元组
        return links, length

    ''' 拿到 page 需爬取的URL; 遍历进入每本小说的详情 page '''
    def details(self, pageNum):
        page_links, length = self.getPage(pageNum)
        for link in page_links:
            # 小说详情 存入字典
            datas = {}
            # 获取网页
            request = requests.get(link)
            # 获取网页内容赋值于变量
            html = request.text
            # 创建 BeautifulSoup对象
            soup = BeautifulSoup(html, 'html.parser')
            # css选择器，通过组合查找; 选出要爬取的区域 | 返回 list
            node = soup.select('div .book_info')[0]

            first_line_node =  node.find_all('dl')[0] # 小说第一行信息
            second_line_node = node.find_all('dl')[1] # 小说第二行信息
            three_line_node = node.find_all('div')[1] # 小说第三行信息
            # 小说详情
            datas['data'] = {
                'title': node.h3.a.string, # 书名
                'grade': node.find_all('div')[0].span.b.font.string, #评分
                'author': first_line_node.find_all('dd')[0].a.string, # 作者
                'type': first_line_node.find_all('dd')[1].a.string, #类型
                'word_number': first_line_node.find_all('dd')[2].string, #字数
                'publish': second_line_node.find_all('dd')[0].string, # 出版社
                'popularity': second_line_node.find_all('dd')[1].string, # 人气
                'price': second_line_node.find_all('dd')[2].string, # 价格
                'collect': three_line_node.find_all('a')[1].find_all('span')[2].string, # 收藏量
                'recommend': three_line_node.find_all('a')[2].span.string, # 推荐量
                'praise': three_line_node.find_all('a')[3].span.string # 大赏量
            }
            # 小说 URL
            datas['spider_url'] = link
            datas['current_page_length'] = length
            # 把 python 对象编码成 JSON 格式, 缩进4格
            data_json = json.dumps(datas, encoding = "UTF-8", ensure_ascii = False, indent = 4)
            print data_json

if __name__ == '__main__':
    base_url = 'http://dushu.qq.com/store/index/sortkey/1/ps/30/p/'
    qq_read = QqRead(base_url)
    # 依次取出 1 - 10, 爬取 1 - 10 页
    for i in range(1, 11):
        qq_read.details(i)


"""
  输出结果：
            正在爬取的网页URL地址: http://dushu.qq.com/store/index/sortkey/1/ps/30/p/1
            本页面共需爬取 30 个URL.
            {
                "spider_url": "http://dushu.qq.com/intro.html?bid=310949",
                "data": {
                    "popularity": "3003",
                    "grade": "3.6",
                    "price": "VIP免费",
                    "word_number": "25万字",
                    "title": "贾宝玉林黛玉别传",
                    "author": "郭洛仁",
                    "publish": "中国科学文化音像出版社限公司",
                    "collect": "3003",
                    "praise": "0",
                    "recommend": "31",
                    "type": "中国古典小说"
                },
                "current_page_length": 30
            }
            {
                "spider_url": "http://dushu.qq.com/intro.html?bid=320438",
                "data": {
                    "popularity": "52255",
                    "grade": "4.2",
                    "price": "5.99元",
                    "word_number": "19万字",
                    "title": "后宫如懿传3",
                    "author": "流潋紫",
                    "publish": "中国华侨出版社",
                    "collect": "52255",
                    "praise": "6",
                    "recommend": "674",
                    "type": "情感"
                },
                "current_page_length": 30
            }
            ......
  """
