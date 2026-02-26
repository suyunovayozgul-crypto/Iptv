import telebot
import requests
import re
import os
import time

TOKEN = "8433156210:AAHxAD_eEpwpOqAhDIDjXVGlhBsKfo9Ow8A"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(func=lambda m: True)
def mass_download(message):
    # Xabardagi barcha havolalarni (http/https) ajratib olish
    urls = re.findall(r'(https?://[^\s]+)', message.text)
    
    if not urls:
        bot.reply_to(message, "📩 Iltimos, pleylist havolalarini yuboring.")
        return

    bot.reply_to(message, f"🚀 {len(urls)} ta havola aniqlandi. Ishlov berishni boshladim...")

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
    }

    for index, url in enumerate(urls):
        try:
            # iLook havolasi bo'lsa, uni yuklash manziliga aylantirish
            if "ilook.epg.one" in url:
                token = re.search(r'ilook\.epg\.one/([A-Z0-9]+)', url).group(1)
                download_url = f"http://itv.one/plist/{token}/all/index.m3u"
            else:
                download_url = url

            # Yuklab olish
            response = requests.get(download_url, headers=headers, timeout=15)
            
            if response.status_code == 200:
                file_name = f"playlist_{index+1}.m3u"
                with open(file_name, "wb") as f:
                    f.write(response.content)
                
                with open(file_name, "rb") as doc:
                    bot.send_document(message.chat.id, doc, caption=f"🔗 Havola: {url}")
                
                os.remove(file_name)
            else:
                bot.send_message(message.chat.id, f"❌ Xatolik ({response.status_code}): {url}")
            
            # Server bloklamasligi uchun kichik tanaffus
            time.sleep(1) 

        except Exception as e:
            bot.send_message(message.chat.id, f"⚠️ Xato: {url}\n{str(e)}")

bot.infinity_polling()
