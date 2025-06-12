from services import EduPlatform
from models import Role
from exporter import Exporter
from scraper import scrape_olx_cars

def print_header(title):
    """Menyular uchun chiroyli sarlavha chiqaradi."""
    print("\n" + "="*40)
    print(f"    {title.upper()}")
    print("="*40)

def admin_menu(platform: EduPlatform):
    # Bu funksiya o'zgarishsiz qoladi, shuning uchun qisqartirilgan
    while True:
        print_header(f"Admin paneli | Foydalanuvchi: {platform._current_user._full_name}")
        print("1. Foydalanuvchi qo'shish")
        print("2. Foydalanuvchini o'chirish")
        print("3. Barcha foydalanuvchilarni ko'rish")
        print("4. Umumiy hisobotni ko'rish")
        print("5. Ma'lumotlarni eksport qilish (XLSX, CSV, SQL)")
        print("6. OLX.UZ'dan ma'lumot qirib olish (Scraping)")
        print("0. Tizimdan chiqish (Logout)")
        choice = input(">>> Tanlovingizni kiriting: ")

        if choice == '1':
            try:
                print("--- Yangi foydalanuvchi qo'shish ---")
                role_choice = input("Rolni tanlang (1-Student, 2-Teacher, 3-Parent, 4-Admin): ")
                role_map = {'1': Role.STUDENT, '2': Role.TEACHER, '3': Role.PARENT, '4': Role.ADMIN}
                if role_choice not in role_map:
                    print("❌ Noto'g'ri rol tanlandi.")
                    continue
                role = role_map[role_choice]
                
                full_name = input("Ism-familiya: ")
                email = input("Email: ")
                password = input("Parol: ")
                
                kwargs = {}
                if role == Role.STUDENT:
                    kwargs['grade_class'] = input("Sinf (masalan, 9-A): ")
                elif role == Role.TEACHER:
                    subjects_str = input("Fanlar (vergul bilan ajratib yozing): ")
                    kwargs['subjects'] = [s.strip() for s in subjects_str.split(',')]
                
                result = platform.admin_add_user(role, full_name, email, password, **kwargs)
                print(result)
            except Exception as e:
                print(f" Xatolik yuz berdi: {e}")

        elif choice == '3':
            print("--- Tizimdagi foydalanuvchilar ---")
            for user in platform.data.users.values():
                print(f"ID: {user._id} | Ism: {user._full_name} | Rol: {user.role.value}")

        elif choice == '4':
            print("--- O'quvchilar bo'yicha hisobot ---")
            report = platform._current_user.generate_report(platform.data.get_all_students())
            print(report)

        elif choice == '5':
            exporter = Exporter(platform.data)
            exporter.export_all()

        elif choice == '6':
            try:
                pages = int(input("Nechta sahifani qirib olish kerak? (masalan, 1): "))
                scrape_olx_cars(pages)
            except ValueError:
                print(" Noto'g'ri raqam kiritildi.")
        
        elif choice == '0':
            break
        else:
            print(" Noto'g'ri tanlov. Qayta urinib ko'ring.")


def teacher_menu(platform: EduPlatform):
    """O'qituvchi uchun menyu va funksiyalar (YANGILANGAN)."""
    while True:
        print_header(f"O'qituvchi paneli | Foydalanuvchi: {platform._current_user._full_name}")
        print("1. Yangi vazifa yaratish")
        print("2. Vazifalarni baholash")
        print("3. Mening xabarnomalarim")
        print("0. Tizimdan chiqish (Logout)")
        choice = input(">>> Tanlovingizni kiriting: ")

        if choice == '1':
            try:
                print("--- Yangi vazifa yaratish ---")
                title = input("Vazifa sarlavhasi: ")
                desc = input("Vazifa tavsifi: ")
                deadline = input("Topshirish muddati (YYYY-MM-DD): ") + "T23:59:59"
                subject = input(f"Fan nomi ({', '.join(platform._current_user.subjects)}): ")
                class_id = input("Sinf (masalan, 9-A): ")
                difficulty = input("Qiyinlik darajasi (oson/o'rta/qiyin): ")
                # --- XATOLIK TO'G'IRLANDI ---
                result = platform.teacher_create_assignment(title, desc, deadline, subject, class_id, difficulty)
                # -------------------------
                print(result)
            except Exception as e:
                print(f" Xatolik: {e}")

        elif choice == '2':
            print("--- Baholanmagan topshiriqlar ---")
            submitted_works = platform.get_submitted_assignments_for_teacher()
            if not submitted_works:
                print("Hozircha baholanmagan topshiriqlar yo'q.")
                continue

            for i, work in enumerate(submitted_works, 1):
                print(f"{i}. O'quvchi: {work['student_name']} | Vazifa: {work['assignment_title']}")
                print(f"   Javob: {work['submission'][:50]}...") # Javobning bir qismini ko'rsatish
            
            try:
                work_choice = int(input("Baholash uchun ish raqamini tanlang (chiqish uchun 0): "))
                if work_choice == 0: continue
                
                selected_work = submitted_works[work_choice - 1]
                grade_value = int(input(f"Bahoni kiriting (1-5) {selected_work['student_name']} uchun: "))
                comment = input("Izoh qoldiring: ")
                
                result = platform.teacher_grade_assignment(
                    selected_work['student_id'],
                    selected_work['assignment_id'],
                    grade_value,
                    comment
                )
                print(result)
            except (ValueError, IndexError):
                print(" Noto'g'ri tanlov yoki raqam kiritildi.")

        elif choice == '3':
            print("--- Xabarnomalar ---")
            print(platform._current_user.view_notifications())
            for n in platform._current_user._notifications: n.mark_as_read()

        elif choice == '0':
            break
        else:
            print(" Noto'g'ri tanlov.")


def student_menu(platform: EduPlatform):
    """O'quvchi uchun menyu va funksiyalar (Yakuniy versiya)."""
    while True:
        print_header(f"O'quvchi paneli | Foydalanuvchi: {platform._current_user._full_name}")
        print("1. Mening vazifalarim")
        print("2. Vazifa topshirish")
        print("3. Baholarimni ko'rish")
        print("4. Baholarim statistikasi (O'rtacha, Eng yuqori, Eng past)")
        print("5. Mening xabarnomalarim")
        print("0. Tizimdan chiqish (Logout)")
        choice = input(">>> Tanlovingizni kiriting: ")
        
        if choice == '4':
            print("--- Baholar statistikasi ---")
            subject_to_analyze = input("Qaysi fan bo'yicha statistika kerak? (Umumiy uchun Enter bosing): ")
            
            # models.py dagi yagona statistik metodni chaqiramiz
            stats = platform._current_user.get_grade_statistics(subject=subject_to_analyze if subject_to_analyze else None)

            if subject_to_analyze:
                print(f"\n--- '{subject_to_analyze}' fani bo'yicha statistika ---")
            else:
                print("\n--- Barcha fanlar bo'yicha umumiy statistika ---")

            if stats['count'] == 0:
                print("Statistika uchun baholar mavjud emas.")
            else:
                print(f"Jami baholar soni: {stats['count']}")
                print(f"O'rtacha baho: {stats['average']:.2f}")
                print(f"Eng yuqori baho: {stats['highest']}")
                print(f"Eng past baho: {stats['lowest']}")
        
        # ... menyuning qolgan qismlari o'zgarishsiz qoladi ...
        elif choice == '1':
            print("--- Mening vazifalarim ---")
            student_assignments = [a for a in platform.data.assignments.values() if a.class_id == platform._current_user.grade_class]
            if not student_assignments:
                print("Sizga berilgan vazifalar mavjud emas.")
            else:
                for assign in student_assignments:
                    status_info = platform._current_user.assignments.get(assign.id)
                    status = "topshirilmagan"
                    if status_info:
                        grade = "baholanmagan"
                        if status_info.get('grade'):
                            grade = status_info['grade'].value
                        status = f"{status_info['status']} (baho: {grade})"
                    print(f"ID: {assign.id} | Mavzu: {assign.title} | Fan: {assign.subject} | Holati: {status}")
        elif choice == '2':
            print("--- Vazifa topshirish ---")
            try:
                assignment_id = int(input("Topshirmoqchi bo'lgan vazifa ID sini kiriting: "))
                if platform._current_user.assignments.get(assignment_id):
                    print("Siz bu vazifani allaqachon topshirgansiz.")
                    continue
                content = input("Javobingizni yozing (500 belgidan oshmasin):\n")
                result = platform.student_submit_assignment(assignment_id, content)
                print(result)
            except ValueError:
                print(" Noto'g'ri ID kiritildi.")
        elif choice == '3':
            print("--- Baholarim ---")
            grades = platform._current_user.view_grades()
            if not grades:
                print("Hozircha baholaringiz yo'q.")
            else:
                for subject, grade_list in grades.items():
                    print(f"{subject}: {grade_list}")
        elif choice == '5':
            print("--- Xabarnomalar ---")
            print(platform._current_user.view_notifications())
            for n in platform._current_user._notifications: n.mark_as_read()
        elif choice == '0':
            break
        else:
            print(" Noto'g'ri tanlov. Qayta urinib ko'ring.")

def parent_menu(platform: EduPlatform):
    """Ota-ona uchun menyu va funksiyalar."""
    parent = platform._current_user
    children_objects = [platform.data.get_user_by_id(child_id) for child_id in parent.children]
    
    while True:
        print_header(f"Ota-ona paneli | Foydalanuvchi: {parent._full_name}")
        print("1. Farzandlarim ro'yxati")
        print("2. Farzandimning baholarini ko'rish")
        print("3. Farzandimning vazifalari holatini ko'rish")
        print("4. Mening xabarnomalarim")
        print("0. Tizimdan chiqish (Logout)")
        choice = input(">>> Tanlovingizni kiriting: ")

        if choice == '1':
            print("--- Sizning farzandlaringiz ---")
            if not children_objects:
                print("Tizimga farzandlaringiz biriktirilmagan.")
            else:
                for child in children_objects:
                    if child:
                        print(f"ID: {child._id} | Ism: {child._full_name} | Sinf: {child.grade_class}")

        elif choice == '2' or choice == '3':
            if not children_objects:
                print("Tizimga farzandlaringiz biriktirilmagan.")
                continue
            
            print("--- Qaysi farzandingiz ma'lumotlarini ko'rmoqchisiz? ---")
            for i, child in enumerate(children_objects, 1):
                if child:
                    print(f"{i}. {child._full_name}")

            try:
                child_choice = int(input("Farzand raqamini tanlang: "))
                if not (1 <= child_choice <= len(children_objects)):
                    print(" Noto'g'ri raqam tanlandi.")
                    continue
                
                selected_child = children_objects[child_choice - 1]

                if choice == '2':
                    print(f"\n--- {selected_child._full_name}ning baholari ---")
                    grades = selected_child.view_grades()
                    if not grades:
                        print("Bu farzandingizning baholari hozircha yo'q.")
                    else:
                        for subject, grade_list in grades.items():
                            print(f"{subject}: {grade_list}")
                
                elif choice == '3':
                    print(f"\n--- {selected_child._full_name}ning vazifalari ---")
                    student_assignments = [a for a in platform.data.assignments.values() if a.class_id == selected_child.grade_class]
                    if not student_assignments:
                        print("Bu farzandingizga berilgan vazifalar mavjud emas.")
                    else:
                        for assign in student_assignments:
                            status_info = selected_child.assignments.get(assign.id)
                            status = "topshirilmagan"
                            if status_info:
                                grade = "baholanmagan"
                                if status_info.get('grade'):
                                    grade = status_info['grade'].value
                                status = f"{status_info['status']} (baho: {grade})"
                            print(f"Mavzu: {assign.title} | Fan: {assign.subject} | Holati: {status}")

            except ValueError:
                print(" Iltimos, raqam kiriting.")

        elif choice == '4':
            print("--- Xabarnomalar ---")
            print(platform._current_user.view_notifications())
            for n in platform._current_user._notifications: n.mark_as_read()
            
        elif choice == '0':
            break
        else:
            print(" Noto'g'ri tanlov.")

# main.py -> main() funksiyasini quyidagicha o'zgartiring

def main():
    """Dasturning asosiy ishga tushish funksiyasi."""
    platform = EduPlatform()
    platform.pre_populate_data()

    while True:
        if not platform._current_user:
            # ... bu qism o'zgarmaydi ...
            print_header("EduPlatform Tizimiga Kirish")
            print("1. Tizimga kirish (Login)")
            print("0. Dasturdan chiqish")
            choice = input(">>> Tanlovingizni kiriting: ")
            
            if choice == '1':
                email = input("Email: ")
                password = input("Parol: ")
                if platform.login(email, password):
                    print(f" Xush kelibsiz, {platform._current_user._full_name}!")
                else:
                    print(" Email yoki parol xato. Qaytadan urinib ko'ring.")
            elif choice == '0':
                print("\n Dasturdan foydalanganingiz uchun rahmat! Xayr!")
                break
        else:
            # --- SHU YERGA O'ZGARTIRISH KIRITILADI ---
            user_role = platform._current_user.role
            if user_role == Role.ADMIN:
                admin_menu(platform)
            elif user_role == Role.TEACHER:
                teacher_menu(platform)
            elif user_role == Role.STUDENT:
                student_menu(platform)
            elif user_role == Role.PARENT: # yangi shartt
        
                parent_menu(platform)
            
            if platform._current_user:
                platform.logout()

if __name__ == "__main__":
    main()