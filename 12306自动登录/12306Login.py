from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import requests
import base64
import re
import time

class Demo():
	def __init__(self):
		self.coordinate=[[-105,-20],[-35,-20],[40,-20],[110,-20],[-105,50],[-35,50],[40,50],[110,50]]
	def login(self):
		login_url="https://kyfw.12306.cn/otn/resources/login.html"
		driver = webdriver.Chrome()
		driver.set_window_size(1200, 900)
		driver.get(login_url)
		time.sleep(1)
		account=driver.find_element_by_class_name("login-hd-account")
		account.click()
		userName=driver.find_element_by_id("J-userName")
		userName.send_keys("15356703166")
		password=driver.find_element_by_id("J-password")
		password.send_keys("31415926zjhh")
		self.driver=driver
	def getVerifyImage(self):
		try:			
			img_element =WebDriverWait(self.driver, 100).until(
				EC.presence_of_element_located((By.ID, "J-loginImg"))
				)
		except Exception :
			print(u"网络开小差,请稍后尝试")	
		base64_str=img_element.get_attribute("src").split(",")[-1]
		imgdata=base64.b64decode(base64_str)
		with open('d:\\verify.jpg','wb') as file:
			file.write(imgdata)
		self.img_element=img_element
	def getVerifyResult(self):
		driver1 = webdriver.Chrome()
		driver1.get('http://littlebigluo.qicp.net:47720/')
		upload = driver1.find_elements_by_tag_name('input')[0]
		time.sleep(3)
		upload.send_keys('d:\\verify.jpg')  # send_keys
		submit = driver1.find_elements_by_tag_name('input')[1].click()
		response=driver1.find_element_by_xpath("/html/body/p[1]/font/font/b").text
		result=[]
		for i in response.split(" "):
			result.append(int(i)-1)
		self.result=result
		driver1.close
		print(result)
	def moveAndClick(self):
		try:
			Action=ActionChains(self.driver)
			for i in self.result:
				Action.move_to_element(self.img_element).move_by_offset(self.coordinate[i][0],self.coordinate[i][1]).click()
			Action.perform()
		except Exception as e:
			print(e)
	def submit(self):
		self.driver.find_element_by_id("J-login").click()
	def __call__(self):
		self.login() 
		time.sleep(3)
		self.getVerifyImage()
		time.sleep(1)
		self.getVerifyResult()
		time.sleep(1)
		self.moveAndClick()
		time.sleep(1)
		self.submit()
		time.sleep(10000)
		
Demo()()
