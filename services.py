from models import *
from data_store import PlatformData

class EduPlatform:
    """
    Bu platformaning asosiy boshqaruv sinfi. Barcha amallar shu yerda bajariladi.
    """
    def __init__(self):
        self.data = PlatformData()  # Ma'lumotlar omborini ishga tushiramiz
        self._current_user = None   # Hozirda tizimga kirgan foydalanuvchi

    def pre_populate_data(self):
        """Dasturni oson test qilish uchun boshlang'ich ma'lumotlarni yaratish funksiyasi."""
        print("  Test uchun boshlang'ich ma'lumotlar yaratilmoqda...")
        
        # Admin
        try:
            admin = Admin("Admin Akmalov", "admin@edu.com", "admin123")
            self.data.add_user(admin)
            
            # O'qituvchi
            teacher = Teacher("Ustoz Olimov", "teacher@edu.com", "teacher123", subjects=["Matematika", "Fizika"])
            teacher.classes = ["9-A"]
            self.data.add_user(teacher)

            # O'quvchilar
            student1 = Student("Ali Valiyev", "ali@edu.com", "student123", "9-A")
            student1.subjects = {"Matematika": teacher._id, "Fizika": teacher._id}
            self.data.add_user(student1)

            student2 = Student("Vali Aliyev", "vali@edu.com", "student456", "9-A")
            student2.subjects = {"Matematika": teacher._id}
            self.data.add_user(student2)

            # Ota-ona
            parent = Parent("Valiyev Ota", "parent@edu.com", "parent123")
            parent.add_child(student1._id)
            parent.add_child(student2._id)
            self.data.add_user(parent)
            
            print(" Test ma'lumotlari muvaffaqiyatli yaratildi.")
        except Exception as e:
            print(f" Test ma'lumotlarini yaratishda xatolik: {e}")

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
        print(f" Xayr, {self._current_user._full_name}!")
        self._current_user = None
    
    # --- ADMIN FUNKSIYALARI ---
    def admin_add_user(self, role: Role, full_name, email, password, **kwargs):
        """Faqat Admin tomonidan yangi foydalanuvchi qo'shish."""
        if not isinstance(self._current_user, Admin):
            return " Xato: Faqat admin foydalanuvchi qo'sha oladi."
        
        if self.data.get_user_by_email(email):
            return f" Xato: '{email}' elektron pochtasi bilan foydalanuvchi allaqachon mavjud."

        new_user = None
        if role == Role.STUDENT:
            grade_class = kwargs.get('grade_class')
            if not grade_class: return " Xato: O'quvchi uchun sinf kiritilishi shart."
            new_user = Student(full_name, email, password, grade_class)
        elif role == Role.TEACHER:
            subjects = kwargs.get('subjects')
            if not subjects: return " Xato: O'qituvchi uchun fanlar ro'yxati kiritilishi shart."
            new_user = Teacher(full_name, email, password, subjects)
        elif role == Role.PARENT:
            new_user = Parent(full_name, email, password)
        elif role == Role.ADMIN:
            new_user = Admin(full_name, email, password)
        
        if new_user:
            self.data.add_user(new_user)
            return f" {role.value} '{full_name}' muvaffaqiyatli qo'shildi."
        return " Xato: Noma'lum rol tanlandi."

    def admin_remove_user(self, user_id_to_remove: int):
        """Faqat Admin tomonidan foydalanuvchini o'chirish."""
        if not isinstance(self._current_user, Admin):
            return " Xato: Faqat admin foydalanuvchi o'chira oladi."
        
        user_to_remove = self.data.get_user_by_id(user_id_to_remove)
        if not user_to_remove:
            return f" Xato: ID={user_id_to_remove} bo'lgan foydalanuvchi topilmadi."
        
        if user_to_remove._id == self._current_user._id:
            return " Xato: Admin o'zini o'chira olmaydi."
            
        self.data.remove_user(user_id_to_remove)
        return f" '{user_to_remove._full_name}' tizimdan muvaffaqiyatli o'chirildi."


    # --- o'qituvci funksiyalari ---
    def teacher_create_assignment(self, title, desc, deadline, subject, class_id, difficulty):
        """Faqat O'qituvchi tomonidan yangi vazifa yaratish."""
        if not isinstance(self._current_user, Teacher):
            return " Xato: Faqat o'qituvchi vazifa yarata oladi."
        
        try:
            # 1 Vazifa obyektini yaratish
            assignment = self._current_user.create_assignment(title, desc, deadline, subject, class_id, difficulty)
            self.data.add_assignment(assignment)
            
            # 2 Shu sinfdagi barcha o'quvchilarga xabarnoma yuborish
            students_in_class = self.data.get_students_by_class(class_id)
            for student in students_in_class:
                notif_msg = f"Yangi vazifa: '{title}' ({subject}). Muddat: {deadline[:10]}"
                notif = Notification(student._id, notif_msg, priority=2)
                student.add_notification(notif)
                
                # 3 Ota-onalarga ham xabar berish (agar yoqilgan bo'lsa)
                parents = [p for p in self.data.users.values() if isinstance(p, Parent) and student._id in p.children]
                for parent in parents:
                    parent_notif_msg = f"Farzandingizga yangi vazifa berildi: '{title}' ({subject})"
                    parent_notif = Notification(parent._id, parent_notif_msg)
                    parent.add_notification(parent_notif)

            return f" Vazifa '{title}' yaratildi va {len(students_in_class)} o'quvchiga yuborildi."
        except ValueError as e:
            return f" Xato: {e}"
        except Exception as e:
            return f" Noma'lum xatolik yuz berdi: {e}"
            
    def teacher_grade_assignment(self, student_id, assignment_id, grade_value, comment):
        """Faqat O'qituvchi tomonidan vazifani baholash."""
        if not isinstance(self._current_user, Teacher):
            return " Xato: Faqat o'qituvchi baho qo'ya oladi."

        student = self.data.get_user_by_id(student_id)
        assignment = self.data.get_assignment_by_id(assignment_id)

        if not student or not isinstance(student, Student):
            return " Xato: Bunday o'quvchi topilmadi."
        if not assignment:
            return " Xato: Bunday vazifa topilmadi."
        
        try:
            result = self._current_user.grade_assignment(student, assignment, grade_value, comment)
            
            # O'quvchiga bahosi haqida xabarnoma yuborish
            notif_msg = f"'{assignment.title}' vazifangiz baholandi: {grade_value}. {comment}"
            priority = 2 if grade_value < 3 else 1 # Agar baho past bo'lsa, muhim xabar
            student.add_notification(Notification(student._id, notif_msg, priority))
            
            return result
        except ValueError as e:
            return f" Xato: {e}"

    # --- o'quvchi funksiyalari ---
    def student_submit_assignment(self, assignment_id: int, content: str):
        """Faqat O'quvchi tomonidan vazifa topshirish."""
        if not isinstance(self._current_user, Student):
            return " Xato: Faqat o'quvchi vazifa topshira oladi."
        
        assignment = self.data.get_assignment_by_id(assignment_id)
        if not assignment:
            return " Xato: Bunday ID bilan vazifa topilmadi."

        # O'quvchining submit_assignment metodini chaqiramiz
        result = self._current_user.submit_assignment(assignment, content)
        
        # O'qituvchiga xabarnoma yuborish
        teacher = self.data.get_user_by_id(assignment.teacher_id)
        if teacher:
            notif_msg = f"O'quvchi {self._current_user._full_name} '{assignment.title}' vazifasini topshirdi."
            teacher.add_notification(Notification(teacher._id, notif_msg))
            
        return result

    # --- yordamci methodlar ---
    def get_submitted_assignments_for_teacher(self):
        """O'qituvchiga tegishli topshirilgan, lekin hali baholanmagan vazifalarni qaytaradi."""
        if not isinstance(self._current_user, Teacher):
            return []

        submitted_works = []
        for assign in self.data.assignments.values():
            # Faqat shu o'qituvchiga tegishli vazifalarni tekshirish
            if assign.teacher_id == self._current_user._id:
                for student_id, submission_content in assign.submissions.items():
                    # Agar bu topshiriq hali baholanmagan bo'lsa
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