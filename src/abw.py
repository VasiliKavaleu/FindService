from selenium import webdriver
from bs4 import BeautifulSoup
import os
import re
import time

class AutoAbw():
	def __init__(self):
		self.info = []
		self.base_url = 'https://avto.abw.by'
		path = os.path.abspath('abw.py')
		base_dir = os.path.dirname(path)
		path_chromedriver = os.path.join(base_dir, 'chromedriver')
		options = webdriver.ChromeOptions()
		options.add_argument('headless')  
		self.browser = webdriver.Chrome(executable_path=path_chromedriver, chrome_options=options)

	def load_page(self, url):
		self.browser.get(url)
		time.sleep(1)
		content = BeautifulSoup(self.browser.page_source, "lxml")
		return content

	def get_info(self, content):
		list_auto = content.select('div.b-adv_list_item ')
		for auto in list_auto:
			title = auto.select_one('div.b-item_title')
			name = title.select_one('a').text.strip()
			href = title.select_one('a').get('href')
			price_not = auto.select_one('div.b-item_price').select_one('span').text
			price = re.search('\d+\s\d*', price_not).group(0)
			desc = auto.select_one('div.b-descr_item_info').text.split()
			fulldesc = ' '.join(desc)
			self.info.append({'name':name,
						'price':price,
						'desc':fulldesc,
						'href': self.base_url + href})
	
	def run_parser(self, url):
		content = self.load_page(url)
		self.get_info(content)
		next = content.select_one('a.next')
		while next:
			url = self.base_url + next.get('href')
			print(url)
			content = self.load_page(url)
			self.get_info(content)
			next = content.select_one('a.next')
		self.browser.quit()
		return self.info


if __name__ == '__main__':
	test = AutoAbw()
	url = 'https://avto.abw.by/minsk/legkovye/prodazha/marka_seat'
	print(len(test.run_parser(url)))