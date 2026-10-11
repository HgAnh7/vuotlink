import os
import requests
import telebot
from bs4 import BeautifulSoup
from urllib.parse import urlparse

BOT_TOKEN = os.getenv("TOKEN")

if not BOT_TOKEN:
    raise ValueError("LỖI: Chưa cấu hình biến môi trường TOKEN")

bot = telebot.TeleBot(BOT_TOKEN)


def get_link2m(alias):
    try:
        cookies = {
            'csrfToken': 'c6069d77ea515b972212a5447a16c62d58fc534981b7a061a3daed119a354f27ecece5534805ae917d767e093b1b281384e92cdb177a31788a65a7a485c8e84d',
            'user_id_7247': 'Q2FrZQ%3D%3D.ZWRlMjRlYWFhYWU5NzI4M2Q3ODczOTlkZTQ3OTNjOWFhNTNiZTk5YWNkZGFkNDhlMjQ5OTc5YmVhOTU3ODZlZvohGO16jA%2BTWE5c0waooIKdtv%2Fc7VLkxIvcVwLk%2FilzxqOGLy%2BCgbKM2ZSTCvuv%2FJ0l1SgtSx8Dn%2FFWAGGaDARu1ptpTAsEDR6pMBEgN8%2BG3%2FjL0qtEUq%2B38WvPXCEZLzwYAprY4T%2Ftgg2SlbJENPGSe8JajBCdUkzJmMdqDLGJfkc2dCRFTIVZjeNcc1YjUDv6bGVcWAryl7thMe%2B5C2ywAv0Lp2i3Gox5H8wEhrpZunShy03L4zIcEDDoDaSks2LdZp5BNZCwyZPW%2B2%2BvkeOTRFCarFl7d3GqZ0ZM7iq49chyvOpfXh49lLuo252yBaaZqKpkd7790k6uZXUa%2BMo%3D',
        }

        headers = {
            'user-agent': 'Mozilla/5.0 (Linux; Android 16; Mobile) AppleWebKit/537.36 Chrome/153.0.8010.36 Mobile Safari/537.36',
            'x-csrf-token': cookies['csrfToken'],
            'x-requested-with': 'XMLHttpRequest',
        }

        response = requests.post(
            'https://vuotlink.xyz/links/gosl/',
            params={'alias': alias},
            cookies=cookies,
            headers=headers,
            timeout=15
        )

        response.raise_for_status()
        data = response.json()

        if not isinstance(data, dict):
            raise ValueError(f"JSON không phải object: {data!r}")

        url = data.get('url')

        if not url:
            raise ValueError(f"API không trả về url: {data!r}")

        print(f"[get_link2m] OK: {url}")
        return url

    except Exception as e:
        print(f"[get_link2m] ERROR: {type(e).__name__}: {e}")
        raise


def get_snote_id(link2m_url):
    try:
        if not link2m_url:
            raise ValueError("URL Link2M đang rỗng")

        response = requests.get(
            link2m_url,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
            },
            timeout=15
        )

        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        h4 = soup.find('h4')

        if not h4:
            raise ValueError(
                f"Không tìm thấy thẻ h4. "
                f"URL cuối: {response.url}; "
                f"HTTP: {response.status_code}"
            )

        note_id = h4.get_text(strip=True).split('|')[0].strip()

        if not note_id:
            raise ValueError("Thẻ h4 không chứa note_id")

        print(f"[get_snote_id] OK: {note_id}")
        return note_id

    except Exception as e:
        print(f"[get_snote_id] ERROR: {type(e).__name__}: {e}")
        raise


def get_snote_content(note_id):
    try:
        if not note_id:
            raise ValueError("note_id đang rỗng")

        url = f'https://note2s.vip/notes/{note_id}'

        response = requests.get(
            url,
            headers={'User-Agent': 'Mozilla/5.0'},
            timeout=15
        )

        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        note = soup.select_one('.form-control.read.content-fit')

        if not note:
            raise ValueError(
                f"Không tìm thấy nội dung. "
                f"HTTP: {response.status_code}; "
                f"URL cuối: {response.url}"
            )

        title_tag = note.find('h5')
        link_tag = note.find('a', href=True)

        if not title_tag:
            raise ValueError("Không tìm thấy tiêu đề h5")

        if not link_tag:
            raise ValueError("Không tìm thấy liên kết href")

        title = title_tag.get_text(strip=True)
        content = link_tag['href']

        result = f"Content:\n{content}\n\nTitle: {title}"
        print(f"[get_snote_content] OK:\n{result}")

        return result

    except Exception as e:
        print(f"[get_snote_content] ERROR: {type(e).__name__}: {e}")
        raise


@bot.message_handler(func=lambda m: True)
def handle_message(message):
    try:
        if not message.text:
            bot.reply_to(message, "Vui lòng gửi URL dạng văn bản.")
            return

        vuotlink_url = message.text.strip()
        parsed = urlparse(vuotlink_url)

        alias = parsed.path.strip('/')

        if not alias:
            raise ValueError("Không lấy được alias từ URL đầu vào")

        print(f"[handle_message] Alias: {alias}")

        link2m_url = get_link2m(alias)
        note_id = get_snote_id(link2m_url)
        result = get_snote_content(note_id)

        bot.reply_to(message, result)

    except Exception as e:
        print(f"[handle_message] ERROR: {type(e).__name__}: {e}")

        try:
            bot.reply_to(
                message,
                f"Đã xảy ra lỗi: {type(e).__name__}\n{e}"
            )
        except Exception as reply_error:
            print(
                f"[reply_to] ERROR: "
                f"{type(reply_error).__name__}: {reply_error}"
            )


if __name__ == "__main__":
    print("[BOT] Starting polling...")

    try:
        bot.infinity_polling(
            timeout=20,
            long_polling_timeout=20,
            skip_pending=False
        )
    except Exception as e:
        print(f"[POLLING] ERROR: {type(e).__name__}: {e}")
        raise