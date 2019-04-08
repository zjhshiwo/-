import requests
import csv
import lxml
from lxml import etree
class Spider:
    def __init__(self,version):
        self.version=version
        self.result=[]

    def get_page(self,start_num):
        url='https://movie.douban.com/top250?start=%s&filter='%start_num
        res=requests.get(url)

        tree=etree.HTML(res.text)
        top250=tree.xpath('//span[@class="title"][1]/text()')
        print(top250)
        return top250
        
    def go(self):
        print('Start...')
        for i in range(0,1):
            top250=self.get_page(i*25)
            self.result += top250
            
        return self.result
if __name__=="__main__":
    my_spider=Spider('1.0')
    res=my_spider.go()
    with open('D:/cs.csv','a+',encoding='UTF-8',newline='')as csvfile:
        w=csv.writer(csvfile)
        w.writerow(res)

