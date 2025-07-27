import requests
from bs4 import BeautifulSoup
import pyodbc
import time


# QIDIRUV PARAMETRLARI
SEARCH_KEYWORD = "data analyst"  # Qidiriladigan kalit so'z (masalan: "java", "python", "accountant")
MAX_PAGES_TO_SCRAPE = 10         # Nechta sahifadan ma'lumot olinishi kerak

# SQL SERVER SOZLAMALARI
# O'zingizning SQL Server ma'lumotlaringizni kiriting
DB_CONFIG = {
    'driver': '{ODBC Driver 17 for SQL Server}',
    'server': 'WIN-A5I5TM5OKQQ\SQLEXPRESS',  # Masalan: 'DESKTOP-ABC\SQLEXPRESS' yoki server IP manzili
    'database': 'JobData',
    'username': 'sa',   # SQL Server foydalanuvchi nomi
    'password': 'turgunboyevv_777'    # SQL Server paroli
    # Agar Windows Authentication ishlatsangiz, username va password o'rniga quyidagini yozing:
    # 'trusted_connection': 'yes'
}



def scrape_saramin(keyword, max_pages):
    """Saramin saytidan ish e'lonlarini yig'adi."""
    all_jobs_data = []
    base_url = "https://www.saramin.co.kr/zf_user/search/recruit"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

    print(f"'{keyword}' bo'yicha ma'lumotlarni yig'ish boshlandi...")

    for page in range(1, max_pages + 1):
        print(f"Sahifa {page} skanerlanmoqda...")
        params = {'searchword': keyword, 'recruitPage': page}
        
        try:
            response = requests.get(base_url, params=params, headers=headers)
            response.raise_for_status()  # HTTP xatoliklarini tekshirish (4xx, 5xx)

            soup = BeautifulSoup(response.text, 'html.parser')
            job_listings = soup.find_all('div', class_='item_recruit')

            if not job_listings:
                print("Bu sahifada boshqa e'lonlar topilmadi. Jarayon to'xtatildi.")
                break

            for job in job_listings:
                title_element = job.find('h2', class_='job_tit')
                company_element = job.find('div', class_='area_corp').find('a', class_='data_layer')
                
                # Joylashuv va boshqa shartlar bitta blokda keladi
                conditions = job.find('div', class_='job_condition').find_all('span')
                location = conditions[0].text.strip() if conditions else 'N/A'

                title = title_element.text.strip() if title_element else 'N/A'
                company = company_element.text.strip() if company_element else 'N/A'
                
                # Havolani olish va to'liq URL'ga aylantirish
                relative_url = title_element.find('a')['href'] if title_element and title_element.find('a') else ''
                job_url = "https://www.saramin.co.kr" + relative_url if relative_url else 'N/A'

                all_jobs_data.append({
                    'title': title,
                    'company': company,
                    'location': location,
                    'url': job_url
                })
        
        except requests.exceptions.RequestException as e:
            print(f"Internetga ulanishda xatolik: {e}")
            break
        except Exception as e:
            print(f"Kutilmagan xatolik yuz berdi: {e}")

        # Saytga og'irlik tushirmaslik uchun har bir so'rovdan keyin kutish
        time.sleep(2)

    print(f"Jami {len(all_jobs_data)} ta ish e'loni topildi.")
    return all_jobs_data



def load_to_sql_server(job_list):
    """Ma'lumotlar ro'yxatini SQL Server bazasiga yuklaydi."""
    if not job_list:
        print("Bazaga yuklash uchun ma'lumotlar mavjud emas.")
        return

    conn_str = (
        f"DRIVER={DB_CONFIG['driver']};"
        f"SERVER={DB_CONFIG['server']};"
        f"DATABASE={DB_CONFIG['database']};"
    )
    if 'trusted_connection' in DB_CONFIG:
        conn_str += f"TRUSTED_CONNECTION={DB_CONFIG['trusted_connection']};"
    else:
        conn_str += f"UID={DB_CONFIG['username']};PWD={DB_CONFIG['password']};"

    conn = None
    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        print("SQL Server'ga muvaffaqiyatli ulanildi.")

        # Takrorlanmaslik uchun mavjud URL'larni tekshirish
        cursor.execute("SELECT JobUrl FROM SaraminJobs")
        existing_urls = {row.JobUrl for row in cursor.fetchall()}
        
        # Faqat yangi ma'lumotlarni filtrlash
        new_jobs = [job for job in job_list if job['url'] not in existing_urls]

        if not new_jobs:
            print("Barcha topilgan ma'lumotlar bazada mavjud. Yangi yozuvlar yo'q.")
            return

        sql_insert_query = """
        INSERT INTO SaraminJobs (JobTitle, CompanyName, Location, JobUrl)
        VALUES (?, ?, ?, ?);
        """
        
        records_to_insert = [
            (job['title'], job['company'], job['location'], job['url']) 
            for job in new_jobs
        ]
        
        cursor.executemany(sql_insert_query, records_to_insert)
        conn.commit()
        
        print(f"Bazaga {cursor.rowcount} ta yangi yozuv muvaffaqiyatli yuklandi.")

    except pyodbc.Error as ex:
        sqlstate = ex.args[0]
        print(f"Ma'lumotlar bazasi bilan ishlashda xatolik yuz berdi: {sqlstate}")
        print(ex)
        
    finally:
        if conn:
            conn.close()
            print("SQL Server bilan aloqa uzildi.")



if __name__ == "__main__":
    # 1-qadam: Saytdan ma'lumotlarni yig'ish
    scraped_data = scrape_saramin(keyword=SEARCH_KEYWORD, max_pages=MAX_PAGES_TO_SCRAPE)
    
    # 2-qadam: Ma'lumotlar mavjud bo'lsa, ularni bazaga yuklash
    if scraped_data:
        load_to_sql_server(scraped_data)
    else:
        print("Jarayon yakunlandi. Hech qanday ma'lumot olinmadi.")