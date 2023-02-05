from django.contrib.auth import views
from django.urls import path
from dept_project import views
from .views import loginaction,stud_dashboard,error,teacher_login_render,home,student_form,teacher_dashboard,teacher_form,stud_dashboard_render,view_submissions,guide_dashboard_render,view_checked_submissions

urlpatterns = [
    path('',home,name = 'home'),
    path('home/',home,name = 'home'),
    path('student_login/',loginaction,name = 'student_login'),
    path('student_dashboard/',stud_dashboard_render,name = "student_dashboard"),
    path('error/',error,name = "error"),
    path('teacher_login',teacher_login_render,name = "teacher_login"),
    path('student_form/',student_form,name="student_form"),
    path('teachers_dashboard/',guide_dashboard_render,name = "teachers_dashboard"),
    path('guide_view_submission/',view_checked_submissions,name = "guide_view_submissions"),
    path('teachers_form/',teacher_form,name = 'teachers_form'),
    path('view_submissions/',stud_dashboard,name='view_submissions')
]