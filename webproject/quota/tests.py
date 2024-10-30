from django.test import TestCase
from .models import Course, Student, User

# Create your tests here.

class QuotaTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="6610681111", password="test123")
        self.student = Student.objects.create(
            name = "Somsak Saksom",
            username = "6610681111",
            user = self.user
            
        )

        self.course = Course.objects.create(
            course_code = "CN543",
            course_name = "Java master",
            course_detail = "Learn about java",
            course_credit = 3,
            course_section = "111000",
            course_remain = 40,
            full = False,
            semester = "1",
            year = "2700"
        )

    def test_course_creation(self):
        self.assertEqual(self.course.course_code, "CN543")
        self.assertEqual(self.course.course_detail, "Learn about java")
        self.assertEqual(self.course.course_section, "111000")
        self.assertEqual(self.course.year, "2700")
        
    def test_student_creation(self):
        self.assertEqual(self.student.username, "6610681111")
        self.assertTrue(self.user.check_password("test123"))
        self.assertEqual(self.student.name, "Somsak Saksom")

    def test_student_str_method(self):
        self.assertEqual(str(self.student), "6610681111 Somsak Saksom")

    def test_course_str_method(self):
        self.assertEqual(str(self.course), "CN543 - Java master")

    def test_password_is_hashed_on_save(self):
        self.assertNotEqual(self.user.password, "test123")
        self.assertTrue(self.user.check_password("test123"))

    def test_check_password(self):
        self.assertTrue(self.user.check_password("test123"))
        self.assertFalse(self.user.check_password("wrong_password"))

