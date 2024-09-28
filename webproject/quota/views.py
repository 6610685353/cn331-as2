from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse

from quota.models import Student
from .models import Course


def all_students(request):
    all_students = Student.objects.all()
    return render(request, "login.html", {"all_students": all_students})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.get_username() == "admin":
                return redirect(reverse("admin:index")) 
            else:
                login(request, user)
                messages.success(request, "Login successful!")
                return redirect("index")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request, "login.html", {"form": form})


@login_required
def index_view(request):
    selected_year = request.GET.get('year')
    selected_semester = request.GET.get('semester')

    all_courses = Course.objects.all()
    if selected_year:
        all_courses = all_courses.filter(year=selected_year)
    if selected_semester:
        all_courses = all_courses.filter(semester=selected_semester)

    context = {
        'all_courses': all_courses,
        'years': sorted(set(Course.objects.values_list('year', flat=True).distinct())),
        'semesters': sorted(set(Course.objects.values_list('semester', flat=True).distinct())),
        'selected_year': selected_year,
        'selected_semester': selected_semester,
    }
    return render(request, 'index.html', context)


@login_required
def academic_year(request):
    return render(request, "academic_year.html")


@login_required
def course_details(request):
    all_courses = Course.objects.all()
    return render(
        request, "course_details.html", {"all_courses": all_courses}
    )  # Fixed key


@login_required
def quota_status(request):
    return render(request, "quota_status.html")


def logout_view(request):
    logout(request)
    messages.success(request, "Logout successful")
    return redirect("login")


@login_required
def enroll_view(request, course_id):
    student = get_object_or_404(Student, user=request.user)
    course = get_object_or_404(Course, id=course_id)

    if course.full:
        messages.error(request, "This course is full.")
        return redirect("course_index")

    if student in course.enrolled_students.all(): 
        messages.error(request, "You are already enrolled in this course.")
        return redirect("quota_status")


    course.enrolled_students.add(student)
    course.course_remain -= 1  
    if course.course_remain <= 0:
        course.full = True 
    course.save()

    messages.success(request, f"Successfully enrolled in {course.course_name}!")
    return redirect("quota_status")


def withdraw_view(request, course_id):
    student = get_object_or_404(Student, user=request.user)
    course = get_object_or_404(Course, id=course_id)

    if request.method == "POST":
        course.enrolled_students.remove(student)
        course.course_remain += 1
        if course.course_remain > 0:
            course.full = False
        course.save()

        messages.success(request, f"Successfully withdrawn from {course.course_name}.")
        return redirect("quota_status")
