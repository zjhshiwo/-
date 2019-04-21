import requests
from lxml import etree


def get_page(start_num):
    url='https://movie.douban.com/top250?start=%s&filter=' %start_num
    res=requests.get(url)

    tree=etree.HTML(res.text)
    top250=tree.xpath('//span[@class="title"][1]/text()')
    print(top250)
    return top250
get_page(0)