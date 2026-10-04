import os
import requests
import telebot
from bs4 import BeautifulSoup
from urllib.parse import urlparse

BOT_TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)


def get_link4m(alias):
	cookies = {
		'csrfToken': 'c6069d77ea515b972212a5447a16c62d58fc534981b7a061a3daed119a354f27ecece5534805ae917d767e093b1b281384e92cdb177a31788a65a7a485c8e84d',
		'user_id_7247': 'Q2FrZQ%3D%3D.ZWRlMjRlYWFhYWU5NzI4M2Q3ODczOTlkZTQ3OTNjOWFhNTNiZTk5YWNkZGFkNDhlMjQ5OTc5YmVhOTU3ODZlZvohGO16jA%2BTWE5c0waooIKdtv%2Fc7VLkxIvcVwLk%2FilzxqOGLy%2BCgbKM2ZSTCvuv%2FJ0l1SgtSx8Dn%2FFWAGGaDARu1ptpTAsEDR6pMBEgN8%2BG3%2FjL0qtEUq%2B38WvPXCEZLzwYAprY4T%2Ftgg2SlbJENPGSe8JajBCdUkzJmMdqDLGJfkc2dCRFTIVZjeNcc1YjUDv6bGVcWAryl7thMe%2B5C2ywAv0Lp2i3Gox5H8wEhrpZunShy03L4zIcEDDoDaSks2LdZp5BNZCwyZPW%2B2%2BvkeOTRFCarFl7d3GqZ0ZM7iq49chyvOpfXh49lLuo252yBaaZqKpkd7790k6uZXUa%2BMo%3D',
	}

	headers = {
		'user-agent': 'Mozilla/5.0 (Linux; Android 16; 24129PN74G Build/BP2A.250605.031.A3; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/153.0.8010.36 Mobile Safari/537.36',
		'x-csrf-token': 'c6069d77ea515b972212a5447a16c62d58fc534981b7a061a3daed119a354f27ecece5534805ae917d767e093b1b281384e92cdb177a31788a65a7a485c8e84d',
		'x-requested-with': 'XMLHttpRequest',
	}

	params = {
		'alias': alias,  # ID lấy từ url người dùng gửi vào bot
	}

	response = requests.post(
'https://vuotlink.xyz/links/gosl/',
		params=params,
		cookies=cookies,
		headers=headers,
	)

	data = response.json()
	return data.get('url')


def get_snote_id(link2m_url):
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
	response = requests.get(link2m_url, headers=headers)
	soup = BeautifulSoup(response.text, 'html.parser')
	h4 = soup.find('h4')
	if h4:
		return h4.get_text().split('|')[0].strip()
	return None


def get_snote_content(note_id):
	url = f'https://note2s.vip/notes/{note_id}'
	
	headers = {
		'User-Agent': 'Mozilla/5.0'
	}
	response = requests.get(url, headers=headers)
	data = response.text

	note = soup.select_one('.form-control.read.content-fit')
	if not note:
		return 'Không tìm thấy nội dung. \nPhiên bản có thể đã cập nhật.'
		
	title = note.find('h5').get_text(strip=True)

	html = note
	soup = BeautifulSoup(str(html), 'html.parser')
	content = soup.a['href'] #
	
	return f'Content:\n{content}\n\nTitle: {title}'

@bot.message_handler(func=lambda m: True)
def handle_message(message):
	vuotlink_url = message.text.strip()  # https://vuotlink.xyz/PvDl -> PvDl là alias
	alias = urlparse(vuotlink_url).path.strip('/')

	link4m_url = get_link2m(alias)
	note_id = get_snote_id(link2m_url)
	result = get_snote_content(note_id)
	bot.reply_to(message, result)

bot.infinity_polling()