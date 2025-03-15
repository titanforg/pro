from telethon import TelegramClient, events
from telethon.tl.types import DocumentAttributeVideo
from yt_dlp import YoutubeDL
import os
import time

# اطلاعات ربات
api_id = 20899157
api_hash = '4a5fed361ed5a8775e0821f3d8e7f571'
bot_token = '7127477593:AAGYqOUqqY0sd_GYaskduYlCLg8cTxs2AJQ'

# ایجاد کلاینت Telethon
client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

# پوشه دانلود
DOWNLOADS_DIR = "downloads"
os.makedirs(DOWNLOADS_DIR, exist_ok=True)

# متغیر برای ذخیره زمان آخرین دانلود
last_download_time = 0

# مسیر فایل کوکی
COOKIES_FILE = "cookies.txt"

def download_instagram_media(url):
    """دانلود ویدیو از اینستاگرام با استفاده از کوکی"""
    options = {
        'outtmpl': f'{DOWNLOADS_DIR}/%(title)s.%(ext)s',
        'quiet': True,
        'format': 'bestvideo+bestaudio/best',
        'noplaylist': True,
        'extract_flat': False,
        'merge_output_format': 'mp4',
        'cookiefile': COOKIES_FILE  # استفاده از کوکی‌ها برای دانلود
    }

    with YoutubeDL(options) as ydl:
        info = ydl.extract_info(url, download=True)
        if not info:
            raise ValueError("اطلاعات ویدیو دریافت نشد!")

        return info, os.path.abspath(ydl.prepare_filename(info))

@client.on(events.NewMessage(pattern=r'/instagram'))
async def request_instagram_link(event):
    """درخواست لینک ویدیو از کاربر"""
    global last_download_time
    current_time = time.time()

    # بررسی محدودیت زمانی بین دانلودها
    if current_time - last_download_time < 30:
        await event.reply("⚠️ برای دانلود بعدی ۳۰ ثانیه صبر کنید.")
        return

    async with client.conversation(event.sender_id) as conv:
        await conv.send_message("🔹 لطفاً لینک ویدیوی اینستاگرام را ارسال کنید.")
        response = await conv.get_response()

        url = response.text.strip()
        if not url.startswith("https://www.instagram.com/"):
            await conv.send_message("⚠️ لطفاً یک لینک معتبر از اینستاگرام ارسال کنید.")
            return

        sent_message = await conv.send_message("📥 در حال دانلود ویدیو... لطفا صبور باشید.")

        try:
            info, file_path = download_instagram_media(url)

            if file_path and os.path.exists(file_path):
                caption = f"🎥 عنوان: {info.get('title', 'ویدیو بدون عنوان')}\n\n⏳ مدت زمان: {int(info.get('duration', 0))} ثانیه\n\n📌 @YourBotUsername"

                await event.client.send_file(
                    event.chat_id,
                    file_path,
                    caption=caption,
                    attributes=[DocumentAttributeVideo(
                        duration=int(info.get("duration", 0)),
                        w=int(info.get("width", 0)),
                        h=int(info.get("height", 0)),
                        supports_streaming=True
                    )]
                )

                await sent_message.delete()
                os.remove(file_path)  # حذف فایل پس از ارسال
                last_download_time = time.time()
            else:
                await sent_message.edit("❌ خطا در یافتن فایل دانلود شده!")

        except Exception as e:
            await sent_message.edit(f"⚠️ خطایی رخ داد: {str(e)}")

client.run_until_disconnected()
