from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import selenium.common.exceptions
import json
import csv
import time
import pymysql

class JdSpider():
    def open_file(self):
        self.fm = input('请输入文件保存格式（txt、json、csv）：')
        while self.fm!='txt' and self.fm!='json' and self.fm!='csv':
            self.fm = input('输入错误，请重新输入文件保存格式（txt、json、csv）：')
        if self.fm=='txt' :
            self.fd = open('D:/Jd.txt','w',encoding='utf-8')
        elif self.fm=='json' :
            self.fd = open('Jd.json','w',encoding='utf-8')
        elif self.fm=='csv' :
            self.fd = open('Jd.csv','w',encoding='utf-8',newline='')

    def open_browser(self):
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(10)
        self.wait = WebDriverWait(self.browser,10)

    def init_variable(self):
        self.data = zip()
        self.isLast = False

    def parse_page(self):
        try:
            skus = self.wait.until(EC.presence_of_all_elements_located((By.XPATH,'//li[@class="gl-item"]')))
            skus = [item.get_attribute('data-sku') for item in skus]
            links = ['https://item.jd.com/{sku}.html'.format(sku=item) for item in skus]
            prices = self.wait.until(EC.presence_of_all_elements_located((By.XPATH,'//div[@class="gl-i-wrap"]/div[3]/strong/i')))
            prices = [item.text for item in prices]
            names = self.wait.until(EC.presence_of_all_elements_located((By.XPATH,'//div[@class="gl-i-wrap"]/div[4]/a/em')))
            names = [item.text for item in names]
            comments = self.wait.until(EC.presence_of_all_elements_located((By.XPATH,'//div[@class="gl-i-wrap"]/div[5]/strong')))
            comments = [item.text for item in comments]
            img_urls = self.wait.until(EC.presence_of_all_elements_located((By.XPATH,'//div[@class="gl-i-wrap"]/div[1]/a/img')))
            img_urls = [item.get_attribute('src') for item in img_urls]
            self.data = zip(links,prices,names,comments,img_urls)
        except selenium.common.exceptions.TimeoutException:
            print('parse_page: TimeoutException1')
            self.parse_page()
        except selenium.common.exceptions.StaleElementReferenceException:
            print('parse_page: StaleElementReferenceException')
            self.browser.refresh()

    def turn_page(self):
        try:
            self.wait.until(EC.element_to_be_clickable((By.XPATH,'//a[@class="pn-next"]'))).click()
            time.sleep(1)
            self.browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            time.sleep(2)
        except selenium.common.exceptions.NoSuchElementException:
            self.isLast = True
        except selenium.common.exceptions.TimeoutException:
            print('turn_page: TimeoutException2')
            self.turn_page()
        except selenium.common.exceptions.StaleElementReferenceException:
            print('turn_page: StaleElementReferenceException')
            self.browser.refresh()

    def write_to_file(self):
        if self.fm == 'txt':
            for item in self.data:
                self.fd.write('----------------------------------------\n')
                self.fd.write('link：' + str(item[0]) + '\n')
                self.fd.write('price：' + str(item[1]) + '\n')
                self.fd.write('name：' + str(item[2]) + '\n')
                self.fd.write('comment：' + str(item[3]) + '\n')
        if self.fm == 'json':
            temp = ('link','price','name','comment')
            for item in self.data:
                json.dump(dict(zip(temp,item)),self.fd,ensure_ascii=False)
        if self.fm == 'csv':
            writer = csv.writer(self.fd)
            for item in self.data:
                writer.writerow(item)
    def write_to_mysql(self):
        db=pymysql.connect("localhost","root","123456","mysql")
        cursor=db.cursor()
        sql="INSERT INTO testmodel_phone(link,price,name,comment,img_url) VALUES (%s,%s,%s,%s,%s)"
        for item in self.data:
            cursor.execute(sql,(item[0],item[1],item[2],item[3],item[4]))
            db.commit()
        db.close()


    def close_file(self):
        self.fd.close()

    def close_browser(self):
        self.browser.quit()

    def crawl(self):
        #self.open_file()
        self.open_browser()
        self.init_variable()
        db=pymysql.connect("localhost","root","123456","mysql")
        cursor=db.cursor()
        sql="truncate table testmodel_phone"
        cursor.execute(sql)
        db.commit()
        db.close()
        print('开始爬取')
        self.browser.get('https://search.jd.com/Search?keyword=%E6%89%8B%E6%9C%BA&enc=utf-8')
        time.sleep(1)
        self.browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        time.sleep(2)
        count = 0
        while count!=2:
            count += 1
            print('正在爬取第 ' + str(count) + ' 页......')
            self.parse_page()
            self.write_to_mysql()
            self.turn_page()
        #self.close_file()
        self.close_browser()
        print('结束爬取')

if __name__ == '__main__':
    spider = JdSpider()
    spider.crawl()
