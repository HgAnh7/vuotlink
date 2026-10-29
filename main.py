import os
import requests
import telebot
from bs4 import BeautifulSoup
from urllib.parse import urlparse

BOT_TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)


def get_link2m(alias):
	cookies = {
	    'refQ6Ec': 'OTAzMGY5M2E3ZDViOTc2MTUyZTY1MWJhOWRjNDEyYWIxZTEyYTE5YjM5YTk5NzAwZTRkYjdjY2Q1N2E2Mjg0YZvsOxCKnXrW0V0k%2FDXZxNiDIspAFzHt72Oxy2HV6jef6HWko4M6hcKjR7oBp%2FbEKw%3D%3D',
	    'app_visitor': '%7B%22ip%22%3A%2227.71.84.88%22%2C%22date%22%3A%222026-10-29+21%3A41%3A55%22%7D',
	    'user_id_7247': '%7B%22array%22%3A%5B%7B%22id%22%3A4073%2C%22views%22%3A2%2C%22max_views%22%3A2%7D%2C%7B%22id%22%3A5166%2C%22views%22%3A1%2C%22max_views%22%3A1%7D%2C%7B%22id%22%3A744%2C%22views%22%3A0%2C%22max_views%22%3A1%7D%5D%2C%22created_at%22%3A%222026-10-29+21%3A41%3A55%22%7D'
	}
	
	headers = {
	    'x-requested-with': 'XMLHttpRequest',
	}
	
	params = {
	    'alias': alias,
	}
	
	response = requests.post('https://link3s.top/links/gosl/', params=params, cookies=cookies, headers=headers, timeout=10)

	result = response.json()
	url = result['data']['url']
	print(url) ####
	return url


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
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    data = response.json()

    note = data.get('note', {})
    title = note.get('title', '')
    soup = BeautifulSoup(note.get('content', ''), 'html.parser')
    link = soup.find('a')
    content = link['href'] if link else soup.get_text(strip=True)

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
