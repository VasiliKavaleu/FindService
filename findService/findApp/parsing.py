from bs4 import BeautifulSoup
import requests

headers = {
		'accept':'*/*','user-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36'
		}

def av(url):
	#url = 'https://cars.av.by/seat/ibiza'
	session = requests.Session()
	info = []
	links = [url]

	req = session.get(url = url, headers=headers)
	if req.status_code == 200:
		content = BeautifulSoup(req.content, "lxml")
		next = content.select_one('a.pages-arrows-link')
		while next.text == 'Следующая страница →':
			url = next.get('href')
			links.append(url)
			req = session.get(url = url, headers=headers)
			if req.status_code == 200:
				content = BeautifulSoup(req.content, "lxml")
				next = content.select('a.pages-arrows-link')
				if len(next) ==2:
					next = next[1]
				else:
					next = next[0]

	for link in links:
		req = session.get(url = link, headers=headers)
		if req.status_code == 200:
			content = BeautifulSoup(req.content, "lxml")
			mainBlock = content.select('div.listing-wrap')
			if mainBlock:
				listAuto = content.select('div.listing-item ')
				for auto in listAuto:
					title = auto.select_one('div.listing-item-title')
					name = title.select_one('a').text.strip()
					href = title.select_one('a').get('href')
					price = auto.select_one('div.listing-item-price').select_one('small').text
					city = auto.select_one('p.listing-item-location').text
					year = auto.select_one('div.listing-item-desc').select_one('span').text
					desc = auto.select_one('div.listing-item-desc').text.split()
					fulldesc = ' '.join(desc)
					info.append({'name':name,
								'price':price,
								'city':city,
								'desc':fulldesc,
								'href':href})
	return info