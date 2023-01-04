from django.contrib.auth import views
from django.urls import path
from dept_project import views
from .views import loginaction,stud_dashboard,error

urlpatterns = [
    path('',loginaction,name = 'login'),
    path('student_dashboard/',stud_dashboard,name = "student_dashboard"),
    path('error/',error,name = "error")
]