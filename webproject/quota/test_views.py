from django.test import TestCase, Client
from django.urls import reverse
from .models import Course, Student, User

class QuotaViewTestCase(TestCase):

    def setUp(self):
        self.client = Client()

        self.login_url = reverse("login")
        self.index_url = reverse("index")
        self.course_details_url = reverse("course_details")
        self.quota_status_url = reverse("quota_status")
        self.quota_academic_year_url = reverse("academic_year")

        self.user = User.objects.create_user(username="6610681111", password="test123")
        self.admin = User.objects.create_user(username="admin", password="adminpass")
        
        self.client.login(username="6610681111", password="test123")

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

    def test_login_view(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "login.html")

    def test_user_login(self):
        response = self.client.get(self.index_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")

    def test_user_not_login(self):
        self.client.logout()
        response = self.client.get(self.index_url)
        self.assertEqual(response.status_code, 302)

    def test_user_invalid_login(self):
        self.client.logout()
        self.client.login(username="6610682222", password="test234")
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)

    def test_login_view_post_valid_message(self):
        response = self.client.post(self.login_url, {"username": "6610681111", "password": "test123"})
        self.assertRedirects(response, self.index_url)
        messages_list = list(response.wsgi_request._messages)
        self.assertEqual(str(messages_list[0]), "Login successful!")

    def test_login_view_post_invalid_message(self):
        response = self.client.post(self.login_url, {"username": "wrong_user", "password": "wrong_pass"})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "login.html")
        messages_list = list(response.wsgi_request._messages)
        self.assertEqual(str(messages_list[0]), "Invalid username or password.")

    def test_admin_login_redirect(self):
        self.client.logout()
        response = self.client.post(self.login_url, {"username": "admin", "password": "adminpass"})
        self.assertEqual(response.status_code, 302)

    def test_index_view_filters_courses(self):
        response = self.client.get(self.index_url, {"year": "2700", "semester": "1"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["all_courses"].count(), 1)

    def test_course_details_view(self):
        response = self.client.get(self.course_details_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "course_details.html")

    def test_quota_status_view(self):
        response = self.client.get(self.quota_status_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "quota_status.html") 

    def test_enroll_view_success(self):
        response = self.client.post(reverse("enroll", args=[self.course.id]))
        self.course.refresh_from_db()
        enrolled_students = self.course.enrolled_students.all()
        self.assertIn(self.student, enrolled_students)
        self.assertEqual(self.course.course_remain, 39)
        self.assertFalse(self.course.full)
        self.assertEqual(response.status_code, 302)

    def test_enroll_view_unsuccess(self):
        self.course.course_remain = 0
        self.course.full = True
        self.course.save()
        response = self.client.post(reverse("enroll", args=[self.course.id]))
        enrolled_students = self.course.enrolled_students.all()
        self.assertNotIn(self.student, enrolled_students)
        self.assertEqual(self.course.course_remain, 0)
        self.assertTrue(self.course.full)
        self.assertEqual(response.status_code, 302) 

    def test_withdraw_view(self):
        response = self.client.post(reverse("enroll", args=[self.course.id]))
        self.course.refresh_from_db()
        enrolled_students = self.course.enrolled_students.all()
        response = self.client.post(reverse("withdraw", args=[self.course.id]))
        self.course.refresh_from_db()
        self.assertNotIn(self.student, enrolled_students)
        self.assertEqual(self.course.course_remain, 40)
        self.assertFalse(self.course.full)
