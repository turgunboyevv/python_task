import os

# Loyiha uchun kerakli fayllar va ularning tavsifi
project_structure = {
    "models.py": "# Bu faylga barcha sinflar (User, Student, Teacher, Assignment va hk) joylashtiriladi.\n",
    "data_store.py": "# Bu faylga ma'lumotlarni xotirada saqlaydigan PlatformData sinfi joylashtiriladi.\n",
    "services.py": "# Bu faylga asosiy biznes mantiq, ya'ni EduPlatform sinfi va uning metodlari yoziladi.\n",
    "exporter.py": "# Bu faylga ma'lumotlarni XLSX, CSV va SQL formatlariga eksport qiluvchi Exporter sinfi yoziladi.\n",
    "scraper.py": "# Bu faylga olx.uz saytidan ma'lumotlarni qirib oluvchi (scraping) funksiya yoziladi.\n",
    "main.py": "# Bu dasturning asosiy ishga tushirish nuqtasi. Foydalanuvchi interfeysi (CLI) shu yerda bo'ladi.\n",
    "README.md": "# Kengaytirilgan EduPlatform Loyihasi (CLI)\n\nLoyiha haqida ma'lumotlar shu yerga yoziladi.",
}

# requirements.txt fayli uchun kerakli kutubxonalar
requirements_content = """pandas
openpyxl
requests
beautifulsoup4
"""

print("🚀 Loyiha fayllarini yaratish boshlandi...")

# Asosiy fayllarni yaratish
for filename, comment in project_structure.items():
    if not os.path.exists(filename):
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(comment)
            print(f"✅ '{filename}' fayli muvaffaqiyatli yaratildi.")
        except IOError as e:
            print(f"❌ '{filename}' faylini yaratishda xatolik: {e}")
    else:
        print(f"⚠️  '{filename}' fayli allaqachon mavjud. O'tkazib yuborildi.")

# requirements.txt faylini yaratish
if not os.path.exists("requirements.txt"):
    try:
        with open("requirements.txt", 'w', encoding='utf-8') as f:
            f.write(requirements_content)
        print("✅ 'requirements.txt' fayli muvaffaqiyatli yaratildi.")
    except IOError as e:
        print(f"❌ 'requirements.txt' faylini yaratishda xatolik: {e}")
else:
    print("⚠️  'requirements.txt' fayli allaqachon mavjud. O'tkazib yuborildi.")

print("\n🎉 Barcha fayllar muvaffaqiyatli yaratildi!")
print("\n--- Keyingi Qadamlar ---")
print("1. Terminalda `pip install -r requirements.txt` buyrug'ini ishga tushirib, kerakli kutubxonalarni o'rnating.")
print("2. Men beradigan keyingi kodlarni mos ravishda yaratilgan fayllarga (`models.py`, `data_store.py` va hk) joylashtiring.")
print("3. Barcha fayllar to'ldirilgach, `python main.py` buyrug'i bilan dasturni ishga tushiring.")