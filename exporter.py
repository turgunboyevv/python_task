# exporter.py
# Bu faylga ma'lumotlarni XLSX, CSV va SQL formatlariga eksport qiluvchi Exporter sinfi yoziladi.

import pandas as pd
import os
from datetime import datetime

# models.py dagi sinflarni import qilish
from models import Student, Teacher, Parent, Admin

class Exporter:
    def __init__(self, platform_data):
        """
        Eksport qiluvchi sinf. Ma'lumotlar omboridan olingan ma'lumotlarni
        turli formatlarga o'giradi.
        """
        self.data = platform_data
        self.export_log = []
        print("ℹ️  Eksport xizmati (v2.0) tayyor.")

    def _log_export(self, format_name: str, path: str):
        """Eksport amaliyotlarini jurnalga yozib boradi."""
        log_entry = f"[{datetime.now().isoformat()}] Format: {format_name}, Manzil: {path}"
        self.export_log.append(log_entry)
        print(f"📄 Log: {log_entry}")

    def _prepare_dataframes(self) -> dict:
        """Ma'lumotlarni to'g'ri formatda Pandas DataFrame'larga o'giradi."""
        
        # 1. Foydalanuvchilar ma'lumotlarini yig'ish
        users_data = []
        for user in self.data.users.values():
            profile = user.get_profile()
            # Rolga qarab qo'shimcha ma'lumotlar
            if isinstance(user, Student):
                profile['Qo\'shimcha'] = f"Sinf: {user.grade_class}"
            elif isinstance(user, Teacher):
                profile['Qo\'shimcha'] = f"Fanlar: {', '.join(user.subjects)}"
            elif isinstance(user, Parent):
                profile['Qo\'shimcha'] = f"Farzandlar soni: {len(user.children)}"
            else:
                profile['Qo\'shimcha'] = ""
            users_data.append(profile)

        # 2. Vazifalar ma'lumotlarini yig'ish
        assignments_data = [
            {
                'ID': assign.id, 'Sarlavha': assign.title, 'Fan': assign.subject,
                'SinfID': assign.class_id, 'Muddat': assign.deadline,
                'Qiyinlik': assign.difficulty, 'OqituvchiID': assign.teacher_id,
                'TopshiriqlarSoni': len(assign.submissions)
            } for assign in self.data.assignments.values()
        ]
            
        # 3. Baholar ma'lumotlarini yig'ish
        grades_data = []
        all_students = self.data.get_all_students()
        for student in all_students:
            for subject_grades in student.grades.values():
                for grade in subject_grades:
                    grades_data.append({
                        'ID': grade.id, 'OquvchiID': grade.student_id, 'Fan': grade.subject,
                        'Baho': grade.value, 'Sana': grade.date, 'OqituvchiID': grade.teacher_id,
                        'Izoh': grade.comment
                    })

        # Bo'sh bo'lmagan DataFrame'larni qaytarish
        dataframes = {
            "Foydalanuvchilar": pd.DataFrame(users_data) if users_data else pd.DataFrame(),
            "Vazifalar": pd.DataFrame(assignments_data) if assignments_data else pd.DataFrame(),
            "Baholar": pd.DataFrame(grades_data) if grades_data else pd.DataFrame()
        }
        return {name: df for name, df in dataframes.items() if not df.empty}

    def export_all(self):
        """Barcha formatlarga birdaniga eksport qiladi."""
        print("\n--- Barcha formatlarga eksport boshlandi ---")
        self.export_to_xlsx()
        self.export_to_csv()
        self.export_to_sql()
        print("--- Eksport yakunlandi ---\n")

    def export_to_xlsx(self, filename: str = "edu_platform_data.xlsx"):
        """Ma'lumotlarni yagona .xlsx faylida, har bir jadvalni alohida varaqda saqlaydi."""
        dfs = self._prepare_dataframes()
        if not dfs:
            print("⚠️ Eksport uchun ma'lumotlar mavjud emas.")
            return

        try:
            with pd.ExcelWriter(filename, engine='openpyxl') as writer:
                for sheet_name, df in dfs.items():
                    df.to_excel(writer, sheet_name=sheet_name, index=False)
            
            full_path = os.path.abspath(filename)
            self._log_export("XLSX", full_path)
            print(f"✅ Ma'lumotlar '{full_path}' fayliga muvaffaqiyatli saqlandi.")
        except Exception as e:
            print(f"❌ XLSX ga eksport qilishda xatolik: {e}")
    
    def export_to_csv(self, directory: str = "csv_export"):
        """Har bir jadvalni alohida .csv fayl qilib, maxsus papkaga saqlaydi."""
        dfs = self._prepare_dataframes()
        if not dfs:
            print("⚠️ Eksport uchun ma'lumotlar mavjud emas.")
            return

        try:
            if not os.path.exists(directory):
                os.makedirs(directory)
            
            for table_name, df in dfs.items():
                file_path = os.path.join(directory, f"{table_name}.csv")
                df.to_csv(file_path, index=False, encoding='utf-8-sig')
            
            full_path = os.path.abspath(directory)
            self._log_export("CSV", full_path)
            print(f"✅ Ma'lumotlar '{full_path}' papkasiga CSV formatida saqlandi.")
        except Exception as e:
            print(f"❌ CSV ga eksport qilishda xatolik: {e}")

    def export_to_sql(self, filename: str = "edu_platform_schema.sql"):
        """SSMS uchun SQL `CREATE TABLE` va `INSERT` so'rovlarini generatsiya qiladi."""
        dfs = self._prepare_dataframes()
        if not dfs:
            print("⚠️ Eksport uchun ma'lumotlar mavjud emas.")
            return

        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"-- EduPlatform uchun SQL Skript\n")
                f.write(f"-- Generatsiya qilingan sana: {datetime.now().isoformat()}\n\n")

                # --- Jadvallarni yaratish (CREATE TABLE) ---
                f.write("-- 1. Jadvallarni yaratish\n")
                f.write("""
CREATE TABLE Users (
    ID BIGINT PRIMARY KEY,
    FullName NVARCHAR(255) NOT NULL,
    Email NVARCHAR(255) UNIQUE,
    Role NVARCHAR(50),
    Phone NVARCHAR(50),
    Address NVARCHAR(MAX),
    RegisteredAt DATETIME,
    ExtraInfo NVARCHAR(MAX)
);

CREATE TABLE Assignments (
    ID BIGINT PRIMARY KEY,
    Title NVARCHAR(255) NOT NULL,
    Subject NVARCHAR(100),
    ClassID NVARCHAR(50),
    Deadline DATETIME,
    Difficulty NVARCHAR(50),
    TeacherID BIGINT,
    SubmissionsCount INT
);

CREATE TABLE Grades (
    ID BIGINT PRIMARY KEY,
    StudentID BIGINT,
    Subject NVARCHAR(100),
    Grade INT CHECK (Grade >= 1 AND Grade <= 5),
    GradeDate DATETIME,
    TeacherID BIGINT,
    Comment NVARCHAR(MAX)
);
\n""")

                # --- Ma'lumotlarni qo'shish (INSERT INTO) ---
                f.write("-- 2. Ma'lumotlarni jadvallarga qo'shish\n")
                for table_name, df in dfs.items():
                    # Jadval nomini SQL uchun moslash
                    sql_table_name_map = {
                        "Foydalanuvchilar": "Users",
                        "Vazifalar": "Assignments",
                        "Baholar": "Grades"
                    }
                    sql_table_name = sql_table_name_map.get(table_name)
                    if not sql_table_name: continue
                    
                    f.write(f"\n-- Ma'lumotlar: {sql_table_name}\n")
                    
                    # Ustun nomlarini moslashtirish
                    df_renamed = df.rename(columns={
                        'Ism-familiya': 'FullName', 'Rol': 'Role', 'Telefon': 'Phone',
                        'Manzil': 'Address', 'Ro\'yxatdan o\'tgan sana': 'RegisteredAt', 'Qo\'shimcha': 'ExtraInfo',
                        'Sarlavha': 'Title', 'Fan': 'Subject', 'SinfID': 'ClassID', 'Muddat': 'Deadline',
                        'Qiyinlik': 'Difficulty', 'OqituvchiID': 'TeacherID', 'TopshiriqlarSoni': 'SubmissionsCount',
                        'OquvchiID': 'StudentID', 'Baho': 'Grade', 'Sana': 'GradeDate', 'Izoh': 'Comment'
                    })

                    for _, row in df_renamed.iterrows():
                        # Qiymatlarni to'g'ri formatlash (NULL va apostroflarni hisobga olish)
                        values = []
                        for val in row.values:
                            if pd.isna(val) or val is None:
                                values.append("NULL")
                            elif isinstance(val, (int, float)):
                                values.append(str(val))
                            else:
                                # Apostroflarni (') ikki barobar qilish
                                cleaned_val = str(val).replace("'", "''")
                                values.append(f"N'{cleaned_val}'")
                        
                        f.write(f"INSERT INTO {sql_table_name} ({', '.join(df_renamed.columns)}) VALUES ({', '.join(values)});\n")

            full_path = os.path.abspath(filename)
            self._log_export("SQL", full_path)
            print(f"✅ SSMS uchun SQL skript '{full_path}' fayliga yozildi.")
        except Exception as e:
            print(f"❌ SQL ga eksport qilishda xatolik: {e}")