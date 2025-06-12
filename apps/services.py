# services.py
# Bu faylga asosiy biznes mantiq, ya'ni EduPlatform sinfi va uning metodlari yoziladi.
# (AVTOMATIK EKSPORT FUNKSIYASI BILAN TO'LIQ VERSIYA)

# Modellar va ma'lumotlar omborini import qilamiz
from models import *
from data_store import PlatformData
from exporter import Exporter # Exporter'ni import qilish

class EduPlatform:
    """
    Bu platformaning asosiy boshqaruv sinfi. Barcha amallar shu yerda bajariladi.
    """
    def __init__(self):
        self.data = PlatformData()
        self._current_user = None

    def pre_populate_data(self):
        """Dasturni oson test qilish uchun boshlang'ich ma'lumotlarni yaratish funksiyasi."""
        print("⚙️  Test uchun boshlang'ich ma'lumotlar yaratilmoqda...")
        try:
            admin = Admin("Admin Akmalov", "admin@edu.com", "admin123")
            self.data.add_user(admin)
            
            teacher = Teacher("Ustoz Olimov", "teacher@edu.com", "teacher123", subjects=["Matematika", "Fizika"])
            teacher.classes = ["9-A"]
            self.data.add_user(teacher)

            student1 = Student("Ali Valiyev", "ali@edu.com", "student123", "9-A")
            student1.subjects = {"Matematika": teacher._id, "Fizika": teacher._id}
            self.data.add_user(student1)

            student2 = Student("Vali Aliyev", "vali@edu.com", "student456", "9-A")
            student2.subjects = {"Matematika": teacher._id}
            self.data.add_user(student2)

            parent = Parent("Valiyev Ota", "parent@edu.com", "parent123")
            parent.add_child(student1._id)
            parent.add_child(student2._id)
            self.data.add_user(parent)
            
            print("✅ Test ma'lumotlari muvaffaqiyatli yaratildi.")
        except Exception as e:
            print(f"❌ Test ma'lumotlarini yaratishda xatolik: {e}")

    def login(self, email: str, password: str) -> bool:
        """Foydalanuvchini email va parol orqali tizimga kiritadi."""
        user = self.data.get_user_by_email(email)
        if user and user._password_hash == hash_password(password):
            self._current_user = user
            return True
        self._current_user = None
        return False

    def logout(self):
        """Joriy foydalanuvchini tizimdan chiqaradi."""
        print(f"👋 Xayr, {self._current_user._full_name}!")
        self._current_user = None

    # --- YORDAMCHI EKSPORT METODI ---
    def _auto_export_data(self):
        """Ma'lumotlar ombori o'zgarganda fayllarni avtomatik yangilaydi."""
        print("\n🔄 Ma'lumotlar ombori o'zgardi. Fayllar yangilanmoqda...")
        try:
            exporter = Exporter(self.data)
            exporter.export_all() # Barcha formatlarga eksport qilish
            print("✅ Fayllar muvaffaqiyatli yangilandi.")
        except Exception as e:
            print(f"❌ Avtomatik eksportda xatolik: {e}")
    # --------------------------------

    # --- ADMIN FUNKSIYALARI ---
    def admin_add_user(self, role: Role, full_name, email, password, **kwargs):
        """Faqat Admin tomonidan yangi foydalanuvchi qo'shadi va avtomatik eksport qiladi."""
        if not isinstance(self._current_user, Admin):
            return "❌ Xato: Faqat admin foydalanuvchi qo'sha oladi."
        
        if self.data.get_user_by_email(email):
            return f"❌ Xato: '{email}' elektron pochtasi bilan foydalanuvchi allaqachon mavjud."

        new_user = None
        try:
            if role == Role.STUDENT:
                grade_class = kwargs.get('grade_class')
                if not grade_class: return "❌ Xato: O'quvchi uchun sinf kiritilishi shart."
                new_user = Student(full_name, email, password, grade_class)
            elif role == Role.TEACHER:
                subjects = kwargs.get('subjects')
                if not subjects: return "❌ Xato: O'qituvchi uchun fanlar ro'yxati kiritilishi shart."
                new_user = Teacher(full_name, email, password, subjects)
            elif role == Role.PARENT:
                new_user = Parent(full_name, email, password)
            elif role == Role.ADMIN:
                new_user = Admin(full_name, email, password)
            else:
                return "❌ Xato: Noma'lum rol tanlandi."

            if new_user:
                self.data.add_user(new_user)
                self._auto_export_data() 
                return f"✅ {role.value} '{full_name}' muvaffaqiyatli qo'shildi va ma'lumotlar fayllarga saqlandi."
                
        except Exception as e:
            return f"❌ Foydalanuvchi yaratishda noma'lum xatolik: {e}"

    def admin_remove_user(self, user_id_to_remove: int):
        """Faqat Admin tomonidan foydalanuvchini o'chiradi va avtomatik eksport qiladi."""
        if not isinstance(self._current_user, Admin):
            return "❌ Xato: Faqat admin foydalanuvchi o'chira oladi."
        
        user_to_remove = self.data.get_user_by_id(user_id_to_remove)
        if not user_to_remove:
            return f"❌ Xato: ID={user_id_to_remove} bo'lgan foydalanuvchi topilmadi."
        
        if user_to_remove._id == self._current_user._id:
            return "❌ Xato: Admin o'zini o'chira olmaydi."
            
        self.data.remove_user(user_id_to_remove)
        self._auto_export_data()
        return f"✅ '{user_to_remove._full_name}' tizimdan muvaffaqiyatli o'chirildi."

    # --- O'QITUVCHI FUNKSIYALARI ---
    def teacher_create_assignment(self, title, desc, deadline, subject, class_id, difficulty):
        """Faqat O'qituvchi tomonidan yangi vazifa yaratish."""
        if not isinstance(self._current_user, Teacher):
            return "❌ Xato: Faqat o'qituvchi vazifa yarata oladi."
        
        try:
            assignment = self._current_user.create_assignment(title, desc, deadline, subject, class_id, difficulty)
            self.data.add_assignment(assignment)
            
            students_in_class = self.data.get_students_by_class(class_id)
            for student in students_in_class:
                notif_msg = f"Yangi vazifa: '{title}' ({subject}). Muddat: {deadline[:10]}"
                notif = Notification(student._id, notif_msg, priority=2)
                student.add_notification(notif)
                
                parents = [p for p in self.data.users.values() if isinstance(p, Parent) and student._id in p.children]
                for parent in parents:
                    parent_notif_msg = f"Farzandingizga yangi vazifa berildi: '{title}' ({subject})"
                    parent_notif = Notification(parent._id, parent_notif_msg)
                    parent.add_notification(parent_notif)
            
            self._auto_export_data() # Vazifa qo'shilganda ham eksport
            return f"✅ Vazifa '{title}' yaratildi va {len(students_in_class)} o'quvchiga yuborildi."
        except ValueError as e:
            return f"❌ Xato: {e}"
        except Exception as e:
            return f"❌ Noma'lum xatolik yuz berdi: {e}"
            
    def teacher_grade_assignment(self, student_id, assignment_id, grade_value, comment):
        """Faqat O'qituvchi tomonidan vazifani baholash."""
        if not isinstance(self._current_user, Teacher):
            return "❌ Xato: Faqat o'qituvchi baho qo'ya oladi."

        student = self.data.get_user_by_id(student_id)
        assignment = self.data.get_assignment_by_id(assignment_id)

        if not student or not isinstance(student, Student):
            return "❌ Xato: Bunday o'quvchi topilmadi."
        if not assignment:
            return "❌ Xato: Bunday vazifa topilmadi."
        
        try:
            result = self._current_user.grade_assignment(student, assignment, grade_value, comment)
            
            notif_msg = f"'{assignment.title}' vazifangiz baholandi: {grade_value}. {comment}"
            priority = 2 if grade_value < 3 else 1
            student.add_notification(Notification(student._id, notif_msg, priority))
            
            self._auto_export_data() # Baho qo'yilganda ham eksport
            return result
        except ValueError as e:
            return f"❌ Xato: {e}"

    # --- O'QUVCHI FUNKSIYALARI ---
    def student_submit_assignment(self, assignment_id: int, content: str):
        """Faqat O'quvchi tomonidan vazifa topshirish."""
        if not isinstance(self._current_user, Student):
            return "❌ Xato: Faqat o'quvchi vazifa topshira oladi."
        
        assignment = self.data.get_assignment_by_id(assignment_id)
        if not assignment:
            return "❌ Xato: Bunday ID bilan vazifa topilmadi."

        result = self._current_user.submit_assignment(assignment, content)
        
        teacher = self.data.get_user_by_id(assignment.teacher_id)
        if teacher:
            notif_msg = f"O'quvchi {self._current_user._full_name} '{assignment.title}' vazifasini topshirdi."
            teacher.add_notification(Notification(teacher._id, notif_msg))
            
        return result

    # --- YORDAMCHI METODLAR ---
    def get_submitted_assignments_for_teacher(self):
        """O'qituvchiga tegishli topshirilgan, lekin hali baholanmagan vazifalarni qaytaradi."""
        if not isinstance(self._current_user, Teacher):
            return []
        submitted_works = []
        for assign in self.data.assignments.values():
            if assign.teacher_id == self._current_user._id:
                for student_id, submission_content in assign.submissions.items():
                    if assign.grades.get(student_id) is None:
                        student = self.data.get_user_by_id(student_id)
                        if student:
                            submitted_works.append({
                                'student_name': student._full_name,
                                'student_id': student_id,
                                'assignment_title': assign.title,
                                'assignment_id': assign.id,
                                'submission': submission_content
                            })
        return submitted_works

    def schedule_add_lesson(self, class_id: str, day: str, time: str, subject: str, teacher_id: int):
        """Dars jadvaliga yangi dars qo'shadi va barcha konfliktlarni tekshiradi."""
        if not isinstance(self._current_user, (Admin, Teacher)):
            return "❌ Xato: Faqat Admin yoki O'qituvchi dars qo'sha oladi."

        for schedule in self.data.schedules.values():
            if schedule.day == day and time in schedule.lessons:
                if schedule.lessons[time]['teacher_id'] == teacher_id:
                    return (f"❌ Konflikt: O'qituvchi (ID: {teacher_id}) bu vaqtda "
                            f"allaqachon '{schedule.class_id}' sinfiga darsga qo'yilgan.")
        
        schedule_key = f"{class_id}_{day}"
        if schedule_key not in self.data.schedules:
            self.data.schedules[schedule_key] = Schedule(class_id, day)
        
        target_schedule = self.data.schedules[schedule_key]

        try:
            target_schedule.add_lesson(time, subject, teacher_id)
            self._auto_export_data() # Dars jadvali o'zgarganda ham eksport
            return f"✅ '{class_id}' sinfining {day} kungi jadvaliga {time}da '{subject}' darsi muvaffaqiyatli qo'shildi."
        except ValueError as e:
            return f"❌ {e}"