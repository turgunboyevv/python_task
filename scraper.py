# Bu faylga olx.uz saytidan ma'lumotlarni qirib oluvchi (scraping) funksiya yoziladi.
# scraper.py
# Bu faylga olx.uz saytidan ma'lumotlarni qirib oluvchi (scraping) funksiya yoziladi.

import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

def scrape_olx_cars(pages: int = 1):
    """
    OLX.uz saytining "Yengil avtomobillar" bo'limidan ma'lumotlarni qirib oladi
    va natijani 'olx_cars_data.csv' fayliga saqlaydi.
    """
    print(f"\n--- OLX.UZ'dan ma'lumotlarni qirib olish boshlandi ({pages} sahifa) ---")
    all_ads = []
    
    # Ba'zi saytlar botlarni bloklaydi, shuning uchun o'zimizni brauzer kabi ko'rsatamiz
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9,uz;q=0.8,ru;q=0.7'
    }

    for page in range(1, pages + 1):
        # OLX sahifalanish (pagination) uchun 'page' parametrini ishlatadi
        url = f"https://www.olx.uz/d/transport/legkovye-avto/?page={page}"
        print(f"🔄 {page}-sahifani yuklanmoqda: {url}")
        
        try:
            response = requests.get(url, headers=headers, timeout=15)
            # Agar so'rov muvaffaqiyatsiz bo'lsa, xabar berib, keyingi sahifaga o'tishga urinmaymiz
            if response.status_code != 200:
                print(f"❌ Xato: Sahifani yuklab bo'lmadi (Status kodi: {response.status_code})")
                break

            soup = BeautifulSoup(response.content, 'html.parser')
            
            # E'lonlar ro'yxatini topish uchun asosiy konteynerni qidiramiz
            # Bu klass nomi OLX sayti o'zgarganda o'zgarishi mumkin
            ads_container = soup.find_all('div', class_='css-1sw7q4x')
            
            if not ads_container:
                print("⚠️ E'lonlar topilmadi. Sayt strukturasi o'zgargan bo'lishi mumkin.")
                break

            for ad in ads_container:
                title_tag = ad.find('h6', class_='css-16v5mdi')
                price_tag = ad.find('p', class_='css-10b0gli')
                location_tag = ad.find('p', class_='css-1a4g99s') # Manzil va sana
                
                # Agar teglar topilmasa, 'N/A' (Not Available) qiymatini beramiz
                title = title_tag.get_text(strip=True) if title_tag else 'N/A'
                price = price_tag.get_text(strip=True) if price_tag else 'N/A'
                location_date = location_tag.get_text(strip=True) if location_tag else 'N/A - N/A'
                
                # Manzil va sanani ajratib olish
                location = location_date.split(' - ')[0]
                date_posted = location_date.split(' - ')[1] if ' - ' in location_date else 'N/A'

                # Ma'lumotlarni tozalash
                # "Договорная" yoki "Обмен" so'zlarini 0 ga tenglashtirish
                if any(word in price for word in ['Договорная', 'Обмен']):
                    cleaned_price = 0
                else:
                    # Narxdan harf va belgilarni olib tashlash
                    cleaned_price = ''.join(filter(str.isdigit, price))
                    cleaned_price = int(cleaned_price) if cleaned_price else 0

                all_ads.append({
                    'Sarlavha': title,
                    'Narxi (so\'m)': cleaned_price,
                    'Manzil': location,
                    'E\'lon sanasi': date_posted
                })
            
            print(f"✅ {page}-sahifadan {len(ads_container)} ta e'lon olindi.")

        except requests.exceptions.RequestException as e:
            print(f"❌ Internetga ulanishda xatolik yuz berdi: {e}")
            break # Ulanish yo'q bo'lsa, tsiklni to'xtatamiz
            
    if not all_ads:
        print("🔴 Yakuniy natija: Hech qanday ma'lumot olinmadi.")
        return

    # Olingan ma'lumotlarni Pandas DataFrame ga o'tkazish
    df = pd.DataFrame(all_ads)
    
    # Duplikatlarni olib tashlash
    df.drop_duplicates(subset=['Sarlavha', 'Narxi (so\'m)', 'Manzil'], inplace=True)
    
    # Fayl nomini sana bilan yaratish
    filename = f"olx_cars_data_{datetime.now().strftime('%Y-%m-%d')}.csv"
    
    # CSV faylga saqlash
    df.to_csv(filename, index=False, encoding='utf-8-sig')
    
    print(f"\n--- Natija ---")
    print(f"🎉 Jami {len(df)} ta unikal e'lon '{filename}' fayliga muvaffaqiyatli saqlandi.")
    print("-------------------------------------------\n")