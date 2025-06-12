from models import Student # Kelajakda kerak bo'lishi mumkin

class PlatformData:
    """
    Ilovaning barcha ma'lumotlarini xotirada (in-memory) saqlash uchun
    markazlashtirilgan sinf. Bu bizning soddalashtirilgan ma'lumotlar bazamiz.
    """
    def __init__(self):
        # Ma'lumotlar lug'atlar (dictionaries) ichida saqlanadi.
        # Kalit -> ID, Qiymat -> Obyektning o'zi.
        self.users = {}         # {user_id: User_obyekti (Student, Teacher, ...)}
        self.assignments = {}   # {assignment_id: Assignment_obyekti}
        self.schedules = {}     # {schedule_id: Schedule_obyekti}
        
        print("ℹ️  Ma'lumotlar ombori (in-memory) muvaffaqiyatli ishga tushirildi.")

    def add_user(self, user_obj):
        """Yangi foydalanuvchi obyektini omborga qo'shadi."""
        if user_obj._id not in self.users:
            self.users[user_obj._id] = user_obj
            return True
        return False

    def get_user_by_id(self, user_id: int):
        """ID orqali foydalanuvchini topib qaytaradi."""
        return self.users.get(user_id)

    def get_user_by_email(self, email: str):
        """Email orqali foydalanuvchini topib qaytaradi."""
        for user in self.users.values():
            if user._email == email:
                return user
        return None
    
    def remove_user(self, user_id: int):
        """Foydalanuvchini ID orqali o'chiradi."""
        if user_id in self.users:
            del self.users[user_id]
            return True
        return False
        
    def add_assignment(self, assignment_obj):
        """Yangi vazifa obyektini omborga qo'shadi."""
        if assignment_obj.id not in self.assignments:
            self.assignments[assignment_obj.id] = assignment_obj
            return True
        return False
        
    def get_assignment_by_id(self, assignment_id: int):
        """ID orqali vazifani topib qaytaradi."""
        return self.assignments.get(assignment_id)

    def get_all_students(self) -> list:
        """Tizimdagi barcha o'quvchilarni ro'yxat qilib qaytaradi."""
        # 'isinstance' yordamida obyektning qaysi sinfga tegishli ekanligini tekshiramiz
        return [user for user in self.users.values() if isinstance(user, Student)]

    def get_students_by_class(self, class_id: str) -> list:
        """Ma'lum bir sinfdagi barcha o'quvchilarni qaytaradi."""
        return [
            student for student in self.get_all_students() 
            if student.grade_class == class_id
        ]