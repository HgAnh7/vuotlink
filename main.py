import os
import requests
import telebot
from bs4 import BeautifulSoup
from urllib.parse import urlparse

BOT_TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)


# =========================
# BƯỚC 1: LẤY LINK 4M
# =========================
def get_link4m(alias):
    try:
        cookies = {
            'csrfToken': '29ff1df9360de0f1fd3b0d637c33c82158c68d6ff58e19a439fc7341d3100451fb6e79a73b9be603783c3ba22146248d7751517c7bd4823e87518ada0fda4b81',
            'user_id_7247': 'Q2FrZQ%3D%3D.Y2I3NjM2ZTE0NmQzZDEzZTFkZmRlMmVmYmVmZDFmY2RhYTg2NTA2NGRkZmY0ZTgyYmZmNTQ3MGZkMGY5ZDJkYzKhP5dmOrjplRx1HQ%2FqugEVEOFzPo5xT9p5xsHi5xzM1GNqfr6cCYsne88Q0qBe0YI4GnnBDecRxcCL8vZMoDdUr8UuJvSnvx8YSIERVc%2FHuv3sBbuno3XoUm2Gv4hCyZyJHsdma1XyQLuLMeg5gDZNCJDXJ2TTLHAVDEAnShGIjEiZ2lPM4catmsmezv7W22%2FsQS%2F6MI%2B56kcViHBDHyHhz1ScTHoVSvcHZy3bqaY7DMZdoXUePA4AdebDCcr3TXYbZivmcAkFBvwkbPUc3Ptt%2F3sMSiRBUwOmF35Gw9Ai%2FieNRosLm8DkzqfFAQ1x5zBdjglC2EVYcHr4WlzebjI%3D',
        }

        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36',
            'x-csrf-token': '29ff1df9360de0f1fd3b0d637c33c82158c68d6ff58e19a439fc7341d3100451fb6e79a73b9be603783c3ba22146248d7751517c7bd4823e87518ada0fda4b81',
            'x-requested-with': 'XMLHttpRequest',
        }

        params = {
            'alias': alias,
        }

        response = requests.post(
            'https://vuotlink.xyz/links/gosl/',
            params=params,
            cookies=cookies,
            headers=headers,
            timeout=15,
        )

        # Kiểm tra HTTP status
        response.raise_for_status()

        # Kiểm tra JSON
        data = response.json()

        url = data.get('url')

        if not url:
            raise ValueError(
                f"API không trả về 'url'. Response: {data}"
            )

        return url

    except requests.exceptions.Timeout:
        raise Exception("Timeout khi kết nối tới vuotlink.xyz")

    except requests.exceptions.HTTPError as e:
        raise Exception(
            f"HTTP Error từ vuotlink.xyz: {e}\n"
            f"Status code: {response.status_code}\n"
            f"Response: {response.text[:500]}"
        )

    except requests.exceptions.RequestException as e:
        raise Exception(f"Lỗi request tới vuotlink.xyz: {e}")

    except ValueError as e:
        raise Exception(f"Lỗi JSON/API vuotlink.xyz: {e}")

    except Exception as e:
        raise Exception(f"Lỗi get_link4m(): {e}")


# =========================
# BƯỚC 2: LẤY NOTE ID
# =========================
def get_snote_id(link4m_url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
        }

        response = requests.get(
            link4m_url,
            headers=headers,
            timeout=15
        )

        response.raise_for_status()

        soup = BeautifulSoup(
            response.text,
            'html.parser'
        )

        title = soup.find('title')

        if not title:
            raise ValueError(
                "Không tìm thấy thẻ <title> trong trang link4m."
            )

        note_id = title.get_text().split('|')[0].strip()

        if not note_id:
            raise ValueError(
                "Không lấy được Note ID từ <title>."
            )

        return note_id

    except requests.exceptions.Timeout:
        raise Exception("Timeout khi truy cập link4m.")

    except requests.exceptions.HTTPError as e:
        raise Exception(
            f"HTTP Error khi truy cập link4m: {e}\n"
            f"Status code: {response.status_code}"
        )

    except requests.exceptions.RequestException as e:
        raise Exception(
            f"Lỗi request tới link4m: {e}"
        )

    except Exception as e:
        raise Exception(f"Lỗi get_snote_id(): {e}")


# =========================
# BƯỚC 3: LẤY NỘI DUNG NOTE
# =========================
def get_snote_content(note_id):
    try:
        url = f'https://note2s.vip/api/notes/{note_id}'

        headers = {
            'User-Agent': 'Mozilla/5.0'
        }

        response = requests.get(
            url,
            headers=headers,
            timeout=15
        )

        response.raise_for_status()

        # Parse JSON
        data = response.json()

        note = data.get('note')

        if not note:
            return (
                'Không tìm thấy nội dung.\n'
                'Phiên bản có thể đã cập nhật.'
            )

        title = note.get('title')

        html = note.get('content')

        if not html:
            raise ValueError(
                "API không trả về trường 'content'."
            )

        soup = BeautifulSoup(
            html,
            'html.parser'
        )

        # Kiểm tra thẻ <a>
        link = soup.find('a')

        if not link:
            raise ValueError(
                "Không tìm thấy thẻ <a> trong content."
            )

        content = link.get('href')

        if not content:
            raise ValueError(
                "Thẻ <a> không có thuộc tính href."
            )

        return (
            f'Content:\n{content}\n\n'
            f'Title: {title}'
        )

    except requests.exceptions.Timeout:
        raise Exception(
            "Timeout khi truy cập API note2s.im."
        )

    except requests.exceptions.HTTPError as e:
        raise Exception(
            f"HTTP Error từ note2s.im: {e}\n"
            f"Status code: {response.status_code}\n"
            f"Response: {response.text[:500]}"
        )

    except requests.exceptions.RequestException as e:
        raise Exception(
            f"Lỗi request tới note2s.im: {e}"
        )

    except ValueError as e:
        raise Exception(
            f"Lỗi JSON/API note2s.im: {e}"
        )

    except Exception as e:
        raise Exception(
            f"Lỗi get_snote_content(): {e}"
        )


# =========================
# XỬ LÝ TIN NHẮN
# =========================
@bot.message_handler(func=lambda m: True)
def handle_message(message):

    try:
        # -------------------------
        # BƯỚC 0: KIỂM TRA URL
        # -------------------------
        try:
            vuotlink_url = message.text.strip()

            if not vuotlink_url:
                raise ValueError("Tin nhắn trống.")

            parsed = urlparse(vuotlink_url)

            if not parsed.path:
                raise ValueError(
                    "Không tìm thấy alias trong URL."
                )

            alias = parsed.path.strip('/')

            if not alias:
                raise ValueError(
                    "Alias rỗng."
                )

        except Exception as e:
            bot.reply_to(
                message,
                f"❌ LỖI BƯỚC 0 - PHÂN TÍCH URL\n\n"
                f"{e}"
            )
            return


        # -------------------------
        # BƯỚC 1: GET LINK 4M
        # -------------------------
        try:
            link4m_url = get_link4m(alias)

        except Exception as e:
            bot.reply_to(
                message,
                f"❌ LỖI BƯỚC 1 - GET LINK4M\n\n"
                f"Alias: {alias}\n\n"
                f"{e}"
            )
            return


        # -------------------------
        # BƯỚC 2: GET NOTE ID
        # -------------------------
        try:
            note_id = get_snote_id(link4m_url)

        except Exception as e:
            bot.reply_to(
                message,
                f"❌ LỖI BƯỚC 2 - GET NOTE ID\n\n"
                f"Link4m:\n{link4m_url}\n\n"
                f"{e}"
            )
            return


        # -------------------------
        # BƯỚC 3: GET CONTENT
        # -------------------------
        try:
            result = get_snote_content(note_id)

        except Exception as e:
            bot.reply_to(
                message,
                f"❌ LỖI BƯỚC 3 - GET NOTE CONTENT\n\n"
                f"Note ID: {note_id}\n\n"
                f"{e}"
            )
            return


        # -------------------------
        # THÀNH CÔNG
        # -------------------------
        bot.reply_to(
            message,
            f"✅ Thành công!\n\n{result}"
        )


    except Exception as e:
        # Lỗi ngoài dự kiến
        bot.reply_to(
            message,
            f"❌ LỖI KHÔNG XÁC ĐỊNH\n\n"
            f"{type(e).__name__}: {e}"
        )


# =========================
# START BOT
# =========================
bot.infinity_polling()