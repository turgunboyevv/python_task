import requests
from bs4 import BeautifulSoup
import csv

# Hedef URL (Python bo‘yicha qidiruv natijalari)
base_url = "https://www.saramin.co.kr/zf_user/search?searchword=python"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(base_url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

# Ish e'lonlarini tanlaymiz
job_posts = soup.select("div.item_recruit")

data = []

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

    data.append([title, company, location, date, link])

# CSV ga yozish
with open("saramin_jobs.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f)
    writer.writerow(["Title", "Company", "Location", "Date", "Link"])
    writer.writerows(data)

print(" Ma'lumotlar saramin_jobs.csv fayliga saqlandi.")
