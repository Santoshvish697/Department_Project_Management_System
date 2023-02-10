from django.contrib.auth import views
from django.urls import path
from dept_project import views
from .views import loginaction,stud_dashboard,error,teacher_login_render,home,student_form,teacher_dashboard,teacher_form,stud_dashboard_render,view_submissions,guide_dashboard_render,view_checked_submissions,admin_dashboard,admin_login,update_table_render,add_user_save,update_table_render,update_student_update_table,update_student_render,search_student_details,form_view,update_student,update_stud,panel_member_render,add_panel_allot

urlpatterns = [
    path('',home,name = 'home'),
    path('home/',home,name = 'home'),
    path('student_login/',loginaction,name = 'student_login'),
    path('student_dashboard/',stud_dashboard_render,name = "student_dashboard"),
    path('error/',error,name = "error"),
    path('teacher_login',teacher_login_render,name = "teacher_login"),
    path('add_student/',student_form,name="student_form"),
    path('teachers_dashboard/',guide_dashboard_render,name = "teachers_dashboard"),
    path('guide_view_submission/',teacher_dashboard,name = "guide_view_submissions"),
    path('teachers_form/',teacher_form,name = 'teachers_form'),
    path('view_submissions/',stud_dashboard,name='view_submissions'),
    path('admin_dashboard/',admin_dashboard,name="admin_dashboard"),
    path('admin_login/',admin_login,name='admin_login'),
    path('add_user/',add_user_save,name = "add_user"),
    path('update_student/',update_student_update_table,name = "update_student"),
    path('update_student_detail/',update_student_render,name = "update_student_detail"),
    path('search_student_details/',search_student_details,name = "search_student_details"),
    path('panel_allot/',panel_member_render,name = "panel_allot"),
    path('add_panel_allot/',add_panel_allot,name = "add_panel_allot")
]