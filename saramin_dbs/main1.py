import requests
from bs4 import BeautifulSoup
import csv
import time
import pyodbc # SQL Server uchun kutubxonani import qilamiz

# ===================================================================
#               >>> SQL SERVER SOZLAMALARI <<<
# ===================================================================
# O'zingizning SQL Server ma'lumotlaringizni kiriting
DB_CONFIG = {
    'driver': '{ODBC Driver 17 for SQL Server}',
    'server': 'WIN-A5I5TM5OKQQ\SQLEXPRESS',  # Masalan: 'DESKTOP-ABC\SQLEXPRESS'
    'database': 'JobData',         # Siz yaratgan baza nomi
    'username': 'sa',
    'password': 'turgunboyevv_777'
    # Agar Windows Authentication ishlatsangiz, username va password o'rniga:
    # 'trusted_connection': 'yes'
}
# ===================================================================

def load_data_to_sql_server(data_to_load):
    """
    Ma'lumotlar ro'yxatini SQL Server bazasiga yuklaydi.
    """
    if not data_to_load:
        print("SQL Server'ga yuklash uchun ma'lumotlar yo'q.")
        return

    conn_str = f"DRIVER={DB_CONFIG['driver']};SERVER={DB_CONFIG['server']};DATABASE={DB_CONFIG['database']};"
    if 'trusted_connection' in DB_CONFIG:
        conn_str += f"TRUSTED_CONNECTION={DB_CONFIG['trusted_connection']};"
    else:
        conn_str += f"UID={DB_CONFIG['username']};PWD={DB_CONFIG['password']};"

    try:
        with pyodbc.connect(conn_str) as conn:
            with conn.cursor() as cursor:
                print("\nSQL Server'ga muvaffaqiyatli ulanildi.")
                
                # Takrorlanmaslik uchun bazadagi mavjud linklarni olamiz
                cursor.execute("SELECT Link FROM SaraminJobsFromCSV")
                existing_links = {row.Link for row in cursor.fetchall()}
                
                # Faqat yangi ma'lumotlarni filtrlash
                # `data_to_load` ro'yxatidagi 4-element (indeks) link hisoblanadi
                new_records = [row for row in data_to_load if row[4] not in existing_links and row[4] != ""]
                
                if not new_records:
                    print("Barcha topilgan ma'lumotlar bazada mavjud. Yangi yozuvlar yo'q.")
                    return

                # SQL so'rovi
                sql_insert_query = """
                INSERT INTO SaraminJobsFromCSV (Title, Company, Location, PostDate, Link)
                VALUES (?, ?, ?, ?, ?);
                """
                
                # `executemany` yordamida barcha yangi yozuvlarni bir martada qo'shamiz
                cursor.executemany(sql_insert_query, new_records)
                conn.commit()
                
                print(f"Bazaga {cursor.rowcount} ta yangi yozuv muvaffaqiyatli yuklandi.")

    except pyodbc.Error as ex:
        print(f"Ma'lumotlar bazasi bilan ishlashda xatolik yuz berdi: {ex}")
    finally:
        print("SQL Server bilan aloqa uzildi.")


# ===================================================================
# >>> BU YERDAN BOSHLAB SIZNING KODINGIZ O'ZGARISHSIZ QOLADI <<<
# ===================================================================

headers = {
    "User-Agent": "Mozilla/5.0"
}

search_keyword = "python"
base_url = "https://www.saramin.co.kr/zf_user/search"

all_data = []

# 1 dan 10-gacha sahifalarni aylantiramiz (istasa, 20+ qilamiz)
for page in range(1, 11):
    print(f" Sahifa: {page}")

    params = {
        "searchword": search_keyword,
        "recruitPage": page,
        "recruitPageCount": 100  # Har sahifada 100 ta e'lon
    }

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

        title = title_tag.text.strip() if title_tag else "Noma'lum"
        link = "https://www.saramin.co.kr" + title_tag['href'] if title_tag else ""
        company = company_tag.text.strip() if company_tag else "Noma'lum"
        location = location_tag.text.strip() if location_tag else "Noma'lum"
        date = date_tag.text.strip() if date_tag else "Noma'lum"

        all_data.append([title, company, location, date, link])

    time.sleep(1)  # Serverga yuklamaslik uchun 1 soniya kutamiz

#  CSV faylga yozamiz (bu qatorni qoldirishingiz yoki olib tashlashingiz mumkin)
with open("saramin_jobs_large.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f)
    writer.writerow(["Title", "Company", "Location", "Date", "Link"])
    writer.writerows(all_data)

print(f" {len(all_data)} ta e'lon 'saramin_jobs_large.csv' fayliga saqlandi.")


# ===================================================================
# >>> YANGI QO'SHILGAN QISM: SQL SERVER'GA YUKLASH <<<
# ===================================================================
if all_data:
    load_data_to_sql_server(all_data)