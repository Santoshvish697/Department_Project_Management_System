from django.shortcuts import render
import mysql.connector as sql
from django.contrib import messages

from dept_project.models import student_input,phase_allot,deliverable_project,diary,panel_members,users,guide
from django.contrib import messages

import mysql.connector


from django.db import connections
# from models import student_input

em=''
pwd=''
login_obj = users()

def home(request):
    return render(request,"DEPARTMENT_PROJECT_MANAGEMENT_SYSTEM/index.html")
def login_redirect(request):
    return render(request,"DEPARTMENT_PROJECT_MANAGEMENT_SYSTEM/login.html")
    

# Create your views here.
def loginaction(request):
    global em,pwd
    print("Connecting")
    if request.method=="POST":
        m=sql.connect(host="127.0.0.1",user="root",passwd="root",database='dept_project')
        cursor=m.cursor()
        d=request.POST
        for key,value in d.items():
            if key=="email":
                em=value
            if key=="password":
                pwd=value
        c="select * from USERS where EMAIL = '{}' and PASSWORD ='{}'".format(em,pwd)
        print(c)
        cursor.execute(c)
        login_obj.email = em
        login_obj.pwd = pwd
        t=tuple(cursor.fetchall())
        if t==():
            messages.info(request, 'Invalid Credentials')
        else:
            dashboard_render = stud_dashboard(request)
            return dashboard_render

    return login_render(request)

def teacher_login_render(request):
    global em,pwd
    print("Connecting")
    if request.method=="POST":
        m=sql.connect(host="127.0.0.1",user="root",passwd="root",database='dept_project')
        cursor=m.cursor()
        d=request.POST
        for key,value in d.items():
            if key=="email":
                em=value
            if key=="password":
                pwd=value
        c="select * from USERS AS U,GUIDE AS G where U.EMAIL = '{}' and U.PASSWORD ='{}' AND G.EMAIL = U.EMAIL".format(em,pwd)
        print(c)
        cursor.execute(c)
        login_obj.email = em
        login_obj.pwd = pwd
        t=tuple(cursor.fetchall())
        if t==():
            messages.info(request, 'Invalid Credentials')
        else:
            dashboard_render = teacher_dashboard(request)
            return dashboard_render
    return render(request,"DEPARTMENT_PROJECT_MANAGEMENT_SYSTEM/teacher_login.html")

def teacher_dashboard(request):
    teacher_dashboard_render = render(request,"DEPARTMENT_PROJECT_MANAGEMENT_SYSTEM/teachers_dashboard.html")
    if (teacher_dashboard_render != None):
        table_render = teacher_table_render(request)
    return table_render

def teacher_table_render(request):
    m=sql.connect(host="127.0.0.1",user="root",passwd="root",database='dept_project')
    cursor=m.cursor()
    cursor.execute("SELECT S.USN, S.FIRST_NAME AS STUDENT_FIRST_NAME, S.LAST_NAME AS STUDENT_LAST_NAME, D.PROJECT_TITLE, D.PROJECT_DOMAIN FROM STUDENT AS S, DELIVERABLE_PROJECT AS D, GUIDE AS G, PANEL_ALLOT AS PA WHERE S.USN = D.USN AND G.USN = S.USN AND G.PROJECT_ID = D.PROJECT_ID AND PA.PANEL_ID = D.PANEL_ID;")
    teacher_data = cursor.fetchall()
    print(teacher_data)
    return render(request, 'DEPARTMENT_PROJECT_MANAGEMENT_SYSTEM/teachers_dashboard.html', {'teacher_data': teacher_data})

def student_form(request):
    if request.method == 'POST':
        m=mysql.connector.connect(host="127.0.0.1",user="root",passwd="root",database='dept_project')
        print("Connecting........")
        cursor=m.cursor()
        d=request.POST
        print("Inserting the values...")
        saverecord = student_input()
        for key,value in d.items():
            if key == 'usn':
                saverecord.usn = d.get('usn')
            if key == 'first-name':
                saverecord.fname = d.get('first-name')
            if key == 'middle-name':
                saverecord.mname = d.get('middle-name')
            if key == 'last-name':
                saverecord.lname = d.get('last-name')
            if key == 'email':
                saverecord.email = d.get('email')
            if key == 'phone':
                saverecord.phone_no = d.get('phone')
        try:
            insert_str = "INSERT INTO STUDENT (USN,First_Name,Middle_Name,Last_Name,Email,Phone_no) VALUES ('{}','{}','{}','{}','{}','{}')".format(saverecord.usn,saverecord.fname,saverecord.mname,saverecord.lname,saverecord.email,saverecord.phone_no)
            cursor.execute(insert_str)
            m.commit()
            m.close()
            messages.success(request,"Details Entered Successfully!")
        except:
            messages.error(request,"Response Recorded or Email Not Registered!")
    return student_form_render(request)



def teacher_form(request):
    if request.method == 'POST':
        m=mysql.connector.connect(host="127.0.0.1",user="root",passwd="root",database='dept_project')
        print("Connecting........")
        cursor=m.cursor()
        d=request.POST
        guide_obj = guide()
        print("Inserting the values...")
        for key,value in d.items():
            if key == 'en_no':
                guide_obj.Guide_ID = d.get('enroll_no')
            if key == 'first-name':
                guide_obj.fname = d.get('first-name')
            if key == 'middle-name':
                guide_obj.mname = d.get('middle-name')
            if key == 'last-name':
                guide_obj.lname = d.get('last-name')
            if key == 'email':
                guide_obj.email = d.get('email')
            if key == 'phone':
                guide_obj.phone_no = d.get('phone')
        try:
            insert_str = "INSERT INTO GUIDE (GUIDE_ID,First_Name,Middle_Name,Last_Name,Email,Phone_no) VALUES ('{}','{}','{}','{}','{}','{}')".format(guide_obj.usn,guide_obj.fname,guide_obj.mname,guide_obj.lname,guide_obj.email,guide_obj.phone_no)
            cursor.execute(insert_str)
            m.commit()
            m.close()
            messages.success(request,"Details Entered Successfully!")
        except:
            messages.error(request,"Response Already Recorded or Email Not Registered!")
    return teacher_form_render(request)
                
    #     if d.get('usn') and d.get('fname') and d.get('mname') and d.get('lname') and d.get('email') and d.get('phone_no'):
    #         saverecord = student_input()
    #         saverecord.usn = d.get('usn')
    #         saverecord.fname = d.get('first-name')
    #         saverecord.mname = d.get('middle-name')
    #         saverecord.lname = d.get('last-name')
    #         saverecord.email = d.get('email')
    #         saverecord.phone_no = d.get('phone')
    #         saverecord.save()
    #         cursor.execute("INSERT INTO STUDENT (USN,First_Name,Middle_Name,Last_Name,Email,Phone_no) VALUES ({},{},{},{},{},{})".format(saverecord.usn,saverecord.fname,saverecord.mname,saverecord.lname,saverecord.email,saverecord.phone_no))
    #         m.commit()
    #         messages.success(request,"Details Entered Successfully!")
    # return student_form_render(request)



def show_table(request):
    m=sql.connect(host="127.0.0.1",user="root",passwd="root",database='dept_project')
    cursor=m.cursor()
    cursor.execute("SELECT PHASE_NO,DUE_DATE,LATE_SUBMISSION FROM PHASE_ALLOT;")
    data = cursor.fetchall()
    return render(request, 'DEPARTMENT_PROJECT_MANAGEMENT_SYSTEM/stud_dashboard.html', {'data': data})


def update_project_details(request):
    m=sql.connect(host="127.0.0.1",user="root",passwd="root",database='dept_project')
    cursor = m.cursor()
    cursor.execute("SELECT D.PROJECT_TITLE,D.PROJECT_DOMAIN,G.FIRST_NAME,G.LAST_NAME FROM DELIVERABLE_PROJECT AS D,STUDENT AS S,USERS AS U,PANEL_ALLOT AS P,GUIDE AS G WHERE D.USN = S.USN AND S.EMAIL = U.EMAIL AND D.PANEL_ID = P.PANEL_ID AND G.GUIDE_ID = P.GUIDE_ID AND U.EMAIL = '{}';".format(login_obj.email))
    title = cursor.fetchall()
    return render(request,'DEPARTMENT_PROJECT_MANAGEMENT_SYSTEM/stud_dashboard.html',{'title': title})


def stud_dashboard(request):
    dashboard_render = render(request,"DEPARTMENT_PROJECT_MANAGEMENT_SYSTEM/stud_dashboard.html")
    if (dashboard_render != None):
        detail_render = update_project_details(request)
        if (detail_render != None):
                table_render = show_table(request)
                return table_render
    return detail_render


def error(request):
    return render(request,"DEPARTMENT_PROJECT_MANAGEMENT_SYSTEM/error.html")

def login_render(request):
    return render(request,"DEPARTMENT_PROJECT_MANAGEMENT_SYSTEM/login.html")

def student_form_render(request):
    return render(request,"DEPARTMENT_PROJECT_MANAGEMENT_SYSTEM/student_form.html")


def teacher_form_render(request):
    return render(request,"DEPARTMENT_PROJECT_MANAGEMENT_SYSTEM/guide_form.html")