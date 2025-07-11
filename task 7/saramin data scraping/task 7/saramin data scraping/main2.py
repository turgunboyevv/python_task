import requests
from bs4 import BeautifulSoup
import csv
import time

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

#  CSV faylga yozamiz
with open("saramin_jobs_large.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f)
    writer.writerow(["Title", "Company", "Location", "Date", "Link"])
    writer.writerows(all_data)

print(f" {len(all_data)} ta e'lon 'saramin_jobs_large.csv' fayliga saqlandi.")
