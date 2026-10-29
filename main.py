import os
import requests
import telebot
from bs4 import BeautifulSoup
from urllib.parse import urlparse

BOT_TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)


def get_link2m(alias):
	cookies = {
	    'lang': 'vi_VN',
	    'refQ6Ec': 'OTAzMGY5M2E3ZDViOTc2MTUyZTY1MWJhOWRjNDEyYWIxZTEyYTE5YjM5YTk5NzAwZTRkYjdjY2Q1N2E2Mjg0YZvsOxCKnXrW0V0k%2FDXZxNiDIspAFzHt72Oxy2HV6jef6HWko4M6hcKjR7oBp%2FbEKw%3D%3D',
	    'app_visitor': '%7B%22ip%22%3A%2227.71.84.88%22%2C%22date%22%3A%222026-10-29+21%3A41%3A55%22%7D',
	    'user_id_7247': '%7B%22array%22%3A%5B%7B%22id%22%3A4073%2C%22views%22%3A2%2C%22max_views%22%3A2%7D%2C%7B%22id%22%3A5166%2C%22views%22%3A1%2C%22max_views%22%3A1%7D%2C%7B%22id%22%3A744%2C%22views%22%3A0%2C%22max_views%22%3A1%7D%5D%2C%22created_at%22%3A%222026-10-29+21%3A41%3A55%22%7D',
	    'ab': '2',
	}
	
	headers = {
	    'accept': 'application/json',
	    'accept-language': 'vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7',
	    'content-type': 'application/x-www-form-urlencoded',
	    'origin': 'https://link3s.top',
	    'priority': 'u=1, i',
	    'referer': 'https://link3s.top/Q6Ec',
	    'sec-ch-ua': '"Not:A-Brand";v="8", "Chromium";v="156", "Android WebView";v="156"',
	    'sec-ch-ua-mobile': '?1',
	    'sec-ch-ua-platform': '"Android"',
	    'sec-fetch-dest': 'empty',
	    'sec-fetch-mode': 'cors',
	    'sec-fetch-site': 'same-origin',
	    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
	    'x-requested-with': 'XMLHttpRequest',
	    # 'cookie': 'lang=vi_VN; refQ6Ec=OTAzMGY5M2E3ZDViOTc2MTUyZTY1MWJhOWRjNDEyYWIxZTEyYTE5YjM5YTk5NzAwZTRkYjdjY2Q1N2E2Mjg0YZvsOxCKnXrW0V0k%2FDXZxNiDIspAFzHt72Oxy2HV6jef6HWko4M6hcKjR7oBp%2FbEKw%3D%3D; app_visitor=%7B%22ip%22%3A%2227.71.84.88%22%2C%22date%22%3A%222026-10-29+21%3A41%3A55%22%7D; user_id_7247=%7B%22array%22%3A%5B%7B%22id%22%3A4073%2C%22views%22%3A2%2C%22max_views%22%3A2%7D%2C%7B%22id%22%3A5166%2C%22views%22%3A1%2C%22max_views%22%3A1%7D%2C%7B%22id%22%3A744%2C%22views%22%3A0%2C%22max_views%22%3A1%7D%5D%2C%22created_at%22%3A%222026-10-29+21%3A41%3A55%22%7D; ab=2',
	}
	
	params = {
	    'alias': alias,
	}
	
	data = {
	    'ad_form_data': 'ZTZiYTRhMGUwYTQxNzQyOWQ5MTk3ZGRiMTBjMDhjZWEzY2NhMThjNzU4MjFkYzE5ZDk0OWE1NmM4ZWRjMGIzNpJ0hZIXxp2O8ZV4AVqNHTDUzx2IXUpnMJDsTRpzRuwGX5QbWfmAigdufjvzXhcLHB9RwnkqjQuwR/6dFmWwf1ShxaQsKyo55jfda6x53xbbnYhAWuJ8BVQIkEvY0Sv5vQjy3wkperRLiae/MDJioFbxGJFqzDZYx6u85pun4u5mxla27xZqDFzDOBxs+KsCbE4Nahn5BCHTYcr3kch0TaKOjhugTlCJIdohYhh+sDXIWvmA2kRR2i8YMuOUgbO1AepuwBOIvbPderleSilaLZ91m5O1Z2AgEJ9LwtWmcIg3KYNTM/V9dj8zMi6dnAmYpYcF4b4a9bDNJhtYD08Jc/MW6qM5gwdnDzh1DCzrQFRf4MRYkfyn7zk99303CD+OPA==',
	}
	
	response = requests.post('https://link3s.top/links/gosl/', params=params, cookies=cookies, headers=headers, data=data, timeout=10)

	data = response.json()
	print(data.get('url')) ####
	return data.get('url')


def get_snote_id(link2m_url):
	headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
	}
	response = requests.get(link2m_url, headers=headers)
	soup = BeautifulSoup(response.text, 'html.parser')
	h4 = soup.find('h4')

	if h4:
		print(h4.get_text().split('|')[0].strip()) ###
		return h4.get_text().split('|')[0].strip()

	return None


def get_snote_content(note_id):
	url = f'https://note2s.vip/notes/{note_id}'
	
	headers = {
		'User-Agent': 'Mozilla/5.0'
	}
	response = requests.get(url, headers=headers)
	soup = BeautifulSoup(response.text, 'html.parser')

	note = soup.select_one('.form-control.read.content-fit')
	if not note:
		return 'Không tìm thấy nội dung. \nPhiên bản có thể đã cập nhật.'
		
	title = note.find('h5').get_text(strip=True)

	html = note
	soup = BeautifulSoup(str(html), 'html.parser')
	content = soup.a['href']
	
	print(f'Content:\n{content}\n\nTitle: {title}') ###
	return f'Content:\n{content}\n\nTitle: {title}'


@bot.message_handler(func=lambda m: True)
def handle_message(message):
	vuotlink_url = message.text.strip()
	alias = urlparse(vuotlink_url).path.strip('/')

	link2m_url = get_link2m(alias)
	note_id = get_snote_id(link2m_url)
	result = get_snote_content(note_id)

	bot.reply_to(message, result)


bot.infinity_polling()