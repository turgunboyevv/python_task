import requests
from bs4 import BeautifulSoup
import csv
import time
import pyodbc
from googletrans import Translator


DB_CONFIG = {
    'driver': '{ODBC Driver 17 for SQL Server}',
    'server': 'WIN-A5I5TM5OKQQ\SQLEXPRESS',
    'database': 'SaraminData_UZ',  # YANGI BAZA NOMI
    'username': 'sa',
    'password': 'turgunboyevv_777'
    # 'trusted_connection': 'yes'
}
# ===================================================================

# Tarjima funksiyasi (O'ZGARISHSIZ)
def translate_to_uzbek(text_to_translate):
    if not text_to_translate or text_to_translate == "Noma'lum": return text_to_translate
    try:
        translator = Translator()
        translated_text = translator.translate(text_to_translate, src='ko', dest='uz').text
        time.sleep(0.3)
        return translated_text
    except Exception as e:
        print(f"Tarjima xatoligi: {e}. Original matn qaytarildi.")
        return text_to_translate

# SQL yuklash funksiyasi (YANGI JADVAL NOMIGA MOSLASHTIRILGAN)
def load_data_to_sql_server(data_to_load):
    if not data_to_load: return
    conn_str = f"DRIVER={DB_CONFIG['driver']};SERVER={DB_CONFIG['server']};DATABASE={DB_CONFIG['database']};"
    if 'trusted_connection' in DB_CONFIG: conn_str += f"TRUSTED_CONNECTION={DB_CONFIG['trusted_connection']};"
    else: conn_str += f"UID={DB_CONFIG['username']};PWD={DB_CONFIG['password']};"
    try:
        with pyodbc.connect(conn_str) as conn:
            with conn.cursor() as cursor:
                print(f"\n'{DB_CONFIG['database']}' bazasiga muvaffaqiyatli ulanildi.")
                
                # JADVAL NOMI O'ZGARTIRILDI: Jobs
                cursor.execute("SELECT Link FROM Jobs")
                existing_links = {row.Link for row in cursor.fetchall()}
                new_records = [row for row in data_to_load if row[4] not in existing_links and row[4] != ""]
                
                if not new_records:
                    print("Barcha topilgan ma'lumotlar bazada mavjud.")
                    return

                # JADVAL VA USTUN NOMLARI O'ZGARTIRILDI
                sql_insert_query = """
                INSERT INTO Jobs (Title_UZ, Company_Original, Location_UZ, PostDate_Original, Link) 
                VALUES (?, ?, ?, ?, ?);
                """
                cursor.executemany(sql_insert_query, new_records)
                conn.commit()
                print(f"'{DB_CONFIG['database']}' bazasidagi 'Jobs' jadvaliga {cursor.rowcount} ta yangi yozuv yuklandi.")
    except pyodbc.Error as ex: print(f"DB xatoligi: {ex}")
    finally: print("SQL Server bilan aloqa uzildi.")


# ... (bu yerdagi asosiy scraping qismi o'zgarishsiz qoladi) ...
headers = {"User-Agent": "Mozilla/5.0"}
search_keyword = "python"
base_url = "https://www.saramin.co.kr/zf_user/search"
all_data = []

for page in range(1, 11): 
    print(f"\nSahifa: {page}")
    params = {"searchword": search_keyword, "recruitPage": page, "recruitPageCount": 100}
    response = requests.get(base_url, headers=headers, params=params)
    soup = BeautifulSoup(response.text, "html.parser")
    job_posts = soup.select("div.item_recruit")
    if not job_posts:
        print("Yana ish e'lonlari topilmadi.")
        break
    for job in job_posts:
        title_tag = job.select_one("h2.job_tit a")
        company_tag = job.select_one("div.area_corp strong a")
        location_tag = job.select_one("div.job_condition span:nth-child(1)")
        date_tag = job.select_one("div.job_date span")
        title_ko = title_tag.text.strip() if title_tag else "Noma'lum"
        link = "https://www.saramin.co.kr" + title_tag['href'] if title_tag else ""
        print(f"Tarjima: '{title_ko[:30]}...'")
        title_uz = translate_to_uzbek(title_ko)
        location_ko = location_tag.text.strip() if location_tag else "Noma'lum"
        location_uz = translate_to_uzbek(location_ko)
        company_original = company_tag.text.strip() if company_tag else "Noma'lum"
        date_original = date_tag.text.strip() if date_tag else "Noma'lum"
        all_data.append([title_uz, company_original, location_uz, date_original, link])
    time.sleep(1)

with open("saramin_jobs_uzbek_fast.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f)
    writer.writerow(["Sarlavha (UZ)", "Kompaniya (Original)", "Joylashuv (UZ)", "Sana (Original)", "Havola"])
    writer.writerows(all_data)
print(f"\n{len(all_data)} ta e'lon 'saramin_jobs_uzbek_fast.csv' fayliga saqlandi.")

if all_data:
    load_data_to_sql_server(all_data)