from django.contrib.auth import views
from django.urls import path
from dept_project import views
from .views import loginaction,stud_dashboard,error,teacher_login_render,home,student_form,teacher_dashboard,teacher_form,stud_dashboard_render,view_submissions,guide_dashboard_render,view_checked_submissions,admin_dashboard,admin_login,update_table_render,add_user_save,update_table_render,update_student_update_table,update_student_render,search_student_details,form_view,update_student,update_stud,panel_member_render,add_panel_allot,internship_guide_render,upload_submission_render

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
    path('panel_allot/',panel_member_render,name = "panel_allot"),
    path('add_panel_allot/',add_panel_allot,name = "add_panel_allot"),
    path('intern_guide_render/',internship_guide_render,name = "internship_guide_render"),
    path('upload_submission/',upload_submission_render,name = "upload_submission"),
    path('edit_student/<str:id>',views.edit_student,name = "edit_student"),
    path('delete_student/<str:id>',views.delete_student,name = "delete_student"),
    path('update_student_final/',views.update_student,name = "update_student_form"),
    path('edit_panel_allot/<str:id>',views.edit_panel_allot,name = "edit_student"),
    path('update_panel_allot/',views.panel_allot_update,name = "update_student_form"),
    path('add_intern_allot/',views.insert_intern,name = "add_intern_allot"),
    path('view_checked_submissions/',views.teacher_dashboard,name = "view_checked_submissions"),
    path('view_unchecked_submissions/',views.unchecked_submit_view,name = "unchecked_view_submissions"),
    path('unchecked_update/<int:id>',views.update_file,name = "unchecked_update"),
    path('add_submission/',views.upload_file,name = "add_submission"),
    path('edit_project_allot/<int:id>',views.edit_project_panel_allot,name= "edit_project_allot"),
    path('project_allot_update/',views.panel_project_update,name = "project_allot_update"),
    path('view_project_panel_allot/',views.panel_project_render,name = "view_project_panel_allot"),
    path('email_feature/',views.email,name = "email_feature"),
    path('guide_add_render/',views.guide_add_render,name = "guide_add"),
    path('add_result_render/<int:id>',views.marks_allot_update,name= "assign_result"),
    path('update_result/',views.marks_allot_update,name = "update_result")
    # path('update_student_details/<int:id>',dept_project.views.student_update,name = "student_update")
]