# scraper.py
# Bu faylga olx.uz saytidan bir nechta kategoriyalar bo'yicha ma'lumotlarni
# qirib oluvchi (scraping) funksiya yoziladi. (TO'LIQ URL MANZILLARI BILAN)

import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import time

# --- HAR BIR KATEGORIYANING TO'LIQ VA ISHLAYDIGAN MANZILI ---
CATEGORIES = [
    {'name': 'Yengil avtomobillar', 'url': 'https://www.olx.uz/d/transport/legkovye-avto/'},
    {'name': 'Kvartiralar (Uzoq muddatli ijara)', 'url': 'https://www.olx.uz/d/nedvizhimost/kvartiry/arenda-dolgosrochnaya/'},
    {'name': 'Telefonlar va Gadjjetlar', 'url': 'https://www.olx.uz/d/elektronika/telefony-i-gadzhety/'},
    {'name': 'Noutbuklar', 'url': 'https://www.olx.uz/d/elektronika/kompyutery/noutbuki/'},
    {'name': 'Bolalar kiyimi', 'url': 'https://www.olx.uz/d/detskiy-mir/detskaya-odezhda/'},
]
# -----------------------------------------------------------------

def scrape_olx_by_categories(items_per_category: int = 2):
    """
    OLX.uz saytidan oldindan belgilangan kategoriyalar bo'yicha ma'lumotlarni
    qirib oladi va yagona CSV faylga saqlaydi.
    """
    print(f"\n--- OLX.UZ'dan kategoriyalar bo'yicha ma'lumotlarni qirib olish boshlandi ---")
    print(f"Har bir kategoriyadan {items_per_category} tadan ma'lumot olinadi.")
    
    all_ads_from_all_categories = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,uz;q=0.6'
    }

    for category in CATEGORIES:
        category_name = category['name']
        url = category['url'] # To'g'ridan-to'g'ri tayyor URL'ni olamiz
        
        print(f"\n🔄 Ishlanmoqda: '{category_name}' kategoriyasi...")
        
        try:
            response = requests.get(url, headers=headers, timeout=15)
            if response.status_code != 200:
                print(f"❌ Xato: '{category_name}' sahifasini yuklab bo'lmadi (Kod: {response.status_code}) - URL: {url}")
                continue

            soup = BeautifulSoup(response.content, 'html.parser')
            # E'lonlar ro'yxatini topish uchun selektor o'zgarmagan
            ads_container = soup.find_all('div', class_='css-1sw7q4x')
            
            if not ads_container:
                print(f"⚠️ '{category_name}' da e'lonlar topilmadi.")
                continue

            count_added = 0
            for ad in ads_container:
                if count_added >= items_per_category:
                    break
                
                title_tag = ad.find('h6', class_='css-16v5mdi')
                price_tag = ad.find('p', class_='css-10b0gli')
                location_tag = ad.find('p', class_='css-1a4g99s')
                
                title = title_tag.get_text(strip=True) if title_tag else 'N/A'
                price = price_tag.get_text(strip=True) if price_tag else 'N/A'
                location_date = location_tag.get_text(strip=True) if location_tag else 'N/A - N/A'
                location = location_date.split(' - ')[0]

                if any(word in price for word in ['Договорная', 'Обмен']):
                    cleaned_price = "Kelishiladi"
                else:
                    cleaned_price = ''.join(filter(str.isdigit, price))
                    cleaned_price = int(cleaned_price) if cleaned_price else 0
                
                all_ads_from_all_categories.append({
                    'Kategoriya': category_name,
                    'Sarlavha': title,
                    'Narxi': cleaned_price,
                    'Manzil': location
                })
                count_added += 1
            
            print(f"✅ '{category_name}' dan {count_added} ta ma'lumot muvaffaqiyatli olindi.")
            time.sleep(1)

        except requests.exceptions.RequestException as e:
            print(f"❌ Internetga ulanishda xatolik: {e}")
            break
            
    if not all_ads_from_all_categories:
        print("\n🔴 Yakuniy natija: Hech qanday ma'lumot olinmadi.")
        return

    df = pd.DataFrame(all_ads_from_all_categories)
    filename = f"olx_multi_category_data_{datetime.now().strftime('%Y-%m-%d')}.csv"
    df.to_csv(filename, index=False, encoding='utf-8-sig')
    
    print(f"\n--- Natija ---")
    print(f"🎉 Jami {len(df)} ta e'lon '{filename}' fayliga muvaffaqiyatli saqlandi.")
    print("-------------------------------------------\n")