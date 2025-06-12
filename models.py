# models.py
# Bu faylga barcha sinflar (User, Student, Teacher, Assignment va hk) joylashtiriladi.

import hashlib
from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum
import time

# --- Yordamchi funksiyalar ---
def generate_id():
    """Dastur ichida unikal ID yaratish uchun oddiy funksiya."""
    return int(time.time() * 10000) + int(time.perf_counter_ns() % 1000)

def hash_password(password: str) -> str:
    """Parolni xavfsiz holatga keltirish (heshlash) uchun funksiya."""
    return hashlib.sha256(password.encode()).hexdigest()

# --- Foydalanuvchi rollari uchun Enum ---
class Role(Enum):
    ADMIN = "Admin"
    TEACHER = "O'qituvchi"
    STUDENT = "O'quvchi"
    PARENT = "Ota-ona"

# --- 1. Abstrakt sinf (boshqa barcha rollar uchun asos) ---
class AbstractRole(ABC):
    def __init__(self, full_name: str, email: str, password: str):
        self._id = generate_id()
        time.sleep(0.001) # ID unikal bo'lishi uchun kichik pauza
        self._full_name = full_name
        self._email = email
        self._password_hash = hash_password(password)
        self._created_at = datetime.now().isoformat()

    @abstractmethod
    def get_profile(self):
        """Foydalanuvchi profili haqida ma'lumot qaytaradi."""
        pass

    @abstractmethod
    def update_profile(self, new_data: dict):
        """Foydalanuvchi profilini yangilaydi."""
        pass

# --- 2. Asosiy Foydalanuvchi sinfi ---
class User(AbstractRole):
    def __init__(self, full_name: str, email: str, password: str, role: Role, phone: str = None, address: str = None):
        super().__init__(full_name, email, password)
        self.role = role
        self.phone = phone
        self.address = address
        self._notifications = []  # Notification obyektlari ro'yxati

    def get_profile(self) -> dict:
        return {
            "ID": self._id,
            "Ism-familiya": self._full_name,
            "Email": self._email,
            "Rol": self.role.value,
            "Telefon": self.phone,
            "Manzil": self.address,
            "Ro'yxatdan o'tgan sana": self._created_at
        }

    def update_profile(self, new_data: dict):
        self._full_name = new_data.get('full_name', self._full_name)
        self.phone = new_data.get('phone', self.phone)
        self.address = new_data.get('address', self.address)
        print(f"✅ '{self._full_name}' profili muvaffaqiyatli yangilandi.")

    def add_notification(self, notification):
        """Foydalanuvchiga yangi xabarnoma qo'shadi."""
        self._notifications.append(notification)

    def view_notifications(self) -> str:
        """Foydalanuvchi xabarnomalarini ko'rsatadi."""
        unread_notifications = [n for n in self._notifications if not n.is_read]
        if not unread_notifications:
            return "Sizda yangi xabarnomalar yo'q."
        # Muhimlik darajasiga qarab saralash (muhimlari tepada)
        sorted_notifications = sorted(unread_notifications, key=lambda n: n.priority, reverse=True)
        return "\n".join([f"[{n.created_at[:10]}] {'❗️(MUHIM) ' if n.priority > 1 else ''}{n.message}" for n in sorted_notifications])

# --- 3. O'quvchi sinfi ---
class Student(User):
    def __init__(self, full_name: str, email: str, password: str, grade_class: str):
        super().__init__(full_name, email, password, Role.STUDENT)
        self.grade_class = grade_class  # masalan, "9-A"
        self.subjects = {}  # {'fan_nomi': oqituvchi_id}
        self.assignments = {}  # {vazifa_id: {'submission': matn, 'status': 'topshirildi', 'grade': Baho_obyekti}}
        self.grades = {}  # {'fan_nomi': [Baho_obyekti_1, Baho_obyekti_2]}

    def submit_assignment(self, assignment, content: str) -> str:
        # Vazifa topshirish cheklovlari
        if len(content) > 500:
            return "❌ Xato: Vazifa matni 500 belgidan oshmasligi kerak."
        
        status = 'topshirildi'
        if datetime.now() > datetime.fromisoformat(assignment.deadline):
            status = 'kechikdi'
        
        self.assignments[assignment.id] = {'submission': content, 'status': status, 'grade': None}
        assignment.add_submission(self._id, content)
        return f"✅ '{assignment.title}' nomli vazifa muvaffaqiyatli topshirildi. Holati: {status}"

# models.py -> class Student

    def view_grades(self, subject: str = None) -> dict:
        # ... bu metod o'zgarishsiz qoladi ...
        if subject:
            if subject not in self.grades:
                return {subject: []}
            return {subject: [g.value for g in self.grades[subject]]}
        return {s: [g.value for g in gl] for s, gl in self.grades.items()}

    # calculate_average_grade METODI O'CHIRIB TASHLANDI

    def get_grade_statistics(self, subject: str = None) -> dict:
        # FAQAT SHU METOD QOLDI
        grades_to_analyze = []
        if subject:
            if subject in self.grades:
                grades_to_analyze = [g.value for g in self.grades[subject]]
        else:
            grades_to_analyze = [g.value for subj_grades in self.grades.values() for g in subj_grades]

        if not grades_to_analyze:
            return {'average': 0.0, 'highest': None, 'lowest': None, 'count': 0}

        return {
            'average': sum(grades_to_analyze) / len(grades_to_analyze),
            'highest': max(grades_to_analyze),
            'lowest': min(grades_to_analyze),
            'count': len(grades_to_analyze)
        }

# --- 4. O'qituvchi sinfi ---
class Teacher(User):
    def __init__(self, full_name: str, email: str, password: str, subjects: list):
        super().__init__(full_name, email, password, Role.TEACHER)
        self.subjects = subjects
        self.classes = []  # ["9-A", "10-B"]
        self.workload = 0 # O'qitish soatlari

    def create_assignment(self, title, description, deadline, subject, class_id, difficulty):
        if subject not in self.subjects:
            raise ValueError(f"Siz '{subject}' fanidan dars bermaysiz.")
        return Assignment(title, description, deadline, subject, self._id, class_id, difficulty)

    def grade_assignment(self, student: Student, assignment, grade_value: int, comment: str):
        if student._id not in assignment.submissions:
            return f"❌ Xato: {student._full_name} bu vazifani topshirmagan."
        
        new_grade = Grade(student._id, assignment.subject, grade_value, self._id, comment)
        
        # Vazifaga baho qo'yish
        assignment.set_grade(student._id, new_grade)
        
        # O'quvchining umumiy baholariga qo'shish
        if assignment.subject not in student.grades:
            student.grades[assignment.subject] = []
        student.grades[assignment.subject].append(new_grade)
        
        return f"✅ {student._full_name}ning '{assignment.title}' vazifasi {grade_value}ga baholandi."
        
# --- 5. Ota-ona sinfi ---
class Parent(User):
    def __init__(self, full_name: str, email: str, password: str):
        super().__init__(full_name, email, password, Role.PARENT)
        self.children = [] # Farzandlarining IDlari ro'yxati
        self.notification_preferences = {'low_grade_alert': True}

    def add_child(self, student_id: int):
        if student_id not in self.children:
            self.children.append(student_id)

    def view_child_grades(self, child: Student):
        print(f"--- {child._full_name}ning baholari ---")
        return child.view_grades()

# --- 6. Admin sinfi ---
class Admin(User):
    def __init__(self, full_name: str, email: str, password: str):
        super().__init__(full_name, email, password, Role.ADMIN)
        self.permissions = ["manage_users", "generate_reports", "export_data"]
    
    def generate_report(self, all_students: list) -> str:
        report = f"Tizim bo'yicha hisobot ({datetime.now().strftime('%Y-%m-%d %H:%M')})\n"
        report += "=" * 50 + "\n"
        if not all_students:
            return "Tizimda o'quvchilar mavjud emas."
            
        for student in all_students:
            avg = student.calculate_average_grade()
            report += f"O'quvchi: {student._full_name} (Sinf: {student.grade_class})\n"
            report += f"  O'rtacha baho: {avg:.2f}\n"
            report += f"  Fanlar bo'yicha baholar: {student.view_grades()}\n"
            report += "-" * 50 + "\n"
        return report

# --- 7. Vazifa sinfi ---
class Assignment:
    def __init__(self, title: str, description: str, deadline: str, subject: str, teacher_id: int, class_id: str, difficulty: str):
        self.id = generate_id()
        time.sleep(0.001)
        self.title = title
        self.description = description
        self.deadline = deadline
        self.subject = subject
        self.teacher_id = teacher_id
        self.class_id = class_id
        self.difficulty = difficulty
        self.submissions = {}  # {student_id: matn}
        self.grades = {}  # {student_id: Baho_obyekti}
    
    def add_submission(self, student_id: int, content: str):
        self.submissions[student_id] = content

    def set_grade(self, student_id: int, grade_obj):
        self.grades[student_id] = grade_obj

# --- 8. Baho sinfi ---
class Grade:
    def __init__(self, student_id: int, subject: str, value: int, teacher_id: int, comment: str = None):
        if not 1 <= value <= 5:
            raise ValueError("Baho 1 dan 5 gacha oraliqda bo'lishi kerak.")
        self.id = generate_id()
        time.sleep(0.001)
        self.student_id = student_id
        self.subject = subject
        self.value = value
        self.date = datetime.now().isoformat()
        self.teacher_id = teacher_id
        self.comment = comment

# --- 9. Dars jadvali sinfi ---
class Schedule:
    def __init__(self, class_id: str, day: str):
        self.id = generate_id()
        time.sleep(0.001)
        self.class_id = class_id
        self.day = day  # "Dushanba", "Seshanba", ...
        self.lessons = {}  # {'08:30': {'subject': 'Matematika', 'teacher_id': 123}}

    def add_lesson(self, time: str, subject: str, teacher_id: int):
        if time in self.lessons:
            # Bir o'qituvchi bir vaqtda boshqa sinfda bo'lmasligini tekshirish kerak
            # Bu mantiqni services.py da amalga oshirgan ma'qul
            raise ValueError(f"{self.class_id} sinfi uchun soat {time}da dars allaqachon mavjud.")
        self.lessons[time] = {"subject": subject, "teacher_id": teacher_id}
        print(f"✅ Jadvalga qo'shildi: {self.day}, {time} - {subject}")

# --- 10. Xabarnoma sinfi ---
class Notification:
    def __init__(self, recipient_id: int, message: str, priority: int = 1):
        self.id = generate_id()
        time.sleep(0.001)
        self.recipient_id = recipient_id
        self.message = message
        self.created_at = datetime.now().isoformat()
        self.is_read = False
        self.priority = priority  # 1: oddiy, 2: muhim
    
    def mark_as_read(self):
        self.is_read = True