from django.urls import path
from . import views

urlpatterns = [
    path("", views.login_view, name="login"),
    path("index/", views.index_view, name="index"),
    path("academic_year/", views.academic_year, name="academic_year"),
    path("course_details/", views.course_details, name="course_details"),
    path("quota_status/", views.quota_status, name="quota_status"),
    path("logout/", views.logout_view, name="logout"),
    path("enroll/<int:course_id>/", views.enroll_view, name="enroll"),
    path("withdraw/<int:course_id>/", views.withdraw_view, name="withdraw"),
    path("quota_status/", views.quota_status, name="quota_status"),
]
