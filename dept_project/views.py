from django.shortcuts import render
import mysql.connector as sql
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
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
            dashboard_render = stud_dashboard_render(request)
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
            dashboard_render = guide_dashboard_render(request)
            return dashboard_render
    return render(request,"DEPARTMENT_PROJECT_MANAGEMENT_SYSTEM/teacher_login.html")

def admin_login(request):
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
            c="select * from USERS AS U where U.EMAIL = 'ise2020@rvce.edu.in' and U.PASSWORD ='{}'".format(pwd)
            print(c)
            cursor.execute(c)
            login_obj.email = em
            login_obj.pwd = pwd
            t=tuple(cursor.fetchall())
            if t==():
                messages.info(request, 'Invalid Credentials')
            else:
                dashboard_render = admin_dashboard(request)
                return dashboard_render
        return render(request,"DEPARTMENT_PROJECT_MANAGEMENT_SYSTEM/teacher_login.html")

def admin_dashboard(request):
    return render(request,"DEPARTMENT_PROJECT_MANAGEMENT_SYSTEM/admin_dashboard.html")

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
    return add_student_render(request)

def add_student_render(request):
    return render(request,'DEPARTMENT_PROJECT_MANAGEMENT_SYSTEM/add_student.html')

def form_view(request):
    return render(request,'DEPARTMENT_PROJECT_MANAGEMENT_SYSTEM/update_student_detail.html')

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
    print(title)
    return render(request,'DEPARTMENT_PROJECT_MANAGEMENT_SYSTEM/stud_dashboard.html',{'title': title})

def teacher_details_update(request):
    m=sql.connect(host="127.0.0.1",user="root",passwd="root",database='dept_project')
    cursor = m.cursor()
    cursor.execute("SELECT FIRST_NAME AS GUIDE_FIRST_NAME,LAST_NAME AS GUIDE_LAST_NAME FROM GUIDE AS G,USERS AS U WHERE G.EMAIL = U.EMAIL AND EMAIL = {};".format(login_obj.email))
    name = cursor.fetchall()
    return render(request,'DEPARTMENT_PROJECT_MANAGEMENT_SYSTEM/stud_dashboard.html',{'name': name})
    

def stud_dashboard(request):
    dashboard_render = render(request,"DEPARTMENT_PROJECT_MANAGEMENT_SYSTEM/stud_dashboard.html")
    if (dashboard_render != None):
        detail_render = update_project_details(request)
        if (detail_render != None):
                table_render = show_table(request)
                return table_render
    return detail_render

def add_user_render(request):
    return render(request,"DEPARTMENT_PROJECT_MANAGEMENT_SYSTEM/add_user.html")

def add_user_save(request):
    if request.method=="POST":
        m=mysql.connector.connect(host="127.0.0.1",user="root",passwd="root",database='dept_project')
        print("Connecting........")
        cursor=m.cursor()
        d=request.POST
        print("Inserting the values...")
        saverecord = users()
        for key,value in d.items():
            if key == 'email':
                saverecord.email = d.get('email')
            if key == 'password':
                saverecord.pwd = d.get('password')
        try:
            insert_str = "INSERT INTO USERS (EMAIL,PASSWORD) VALUES ('{}','{}')".format(saverecord.email,saverecord.pwd)
            cursor.execute(insert_str)
            m.commit()
            m.close()
            messages.success(request,"Details Entered Successfully!")
        except:
            messages.error(request,"Error")
            user_render = add_user_render(request)
            return user_render
    return add_user_render(request)


#UPDATE DB OPERATIONS
def update_student_render(request):
    update_student_detail_render = render(request,"DEPARTMENT_PROJECT_MANAGEMENT_SYSTEM/update_student_detail.html")
    if (update_student_detail_render != None):
        search_render = search_student_details(request)
        if(search_render != None):
            update_student_submit = update_student(request)
        return search_render
      
def search_student_details(request):
    if request.method == "POST":
        m = mysql.connector.connect(host="127.0.0.1",user="root",passwd="root",database='dept_project')
        print("Connected to DB")
        cursor = m.cursor()
        d = request.POST
        saverecord = student_input()
        for key,value in d.items():
            if key == 'usn':
                saverecord.usn = d.get('usn')
        try:
            print(saverecord.usn)
            search_str = "SELECT FIRST_NAME,MIDDLE_NAME,LAST_NAME,EMAIL,PHONE_NO,USN FROM STUDENT WHERE USN = '{}';".format(saverecord.usn)
            cursor.execute(search_str)
            student_form_details = cursor.fetchall()
            print(student_form_details)
            if "search_student" in request.POST:
                return render(request,"DEPARTMENT_PROJECT_MANAGEMENT_SYSTEM/update_student_detail.html",{"student_form_data" : student_form_details})
        except:
            messages.error(request,"Could Not Render Student Details with this USN")
            update_view = form_view(request)
            return update_view
    return form_view(request)

def update_student(request):
    if request.method=="POST":
        m=mysql.connector.connect(host="127.0.0.1",user="root",passwd="root",database='dept_project')
        cursor=m.cursor()
        d=request.POST
        print(em)
        for key,value in d.items():
            if key == 'usn':
                usn_no = d.get('usn')
                print(usn_no)
            if key == 'fname':
                first_name = d.get('fname')
            if key == 'mname':
                middle_name = d.get('mname')
            if key == 'lname':
                last_name = d.get('lname')
            if key == 'phone_no':
                phone_no = d.get('phone_no')
        try:
            user = student_input.objects.get(id= usn_no)
            print("Object Found")
            user.fname = first_name
            user.mname = middle_name
            user.lname = last_name
            user.phone_no = phone_no
            user.save()
            print("Edited!")
            messages.success(request,"Successfully Edited Student")
        except:
            messages.error(request,"Error in Table Updation")
            user_render = update_table_render(request)
    return form_view(request)
 
def update_stud(request,id):
    students = students.objects.get(usn = id)
    return render(request,'DEPARTMENT_PROJECT_MANAGEMENT_SYSTEM/update_stud.html',{'students' : students})
   
def panel_member_render(request):
    m=sql.connect(host="127.0.0.1",user="root",passwd="root",database='dept_project')
    cursor = m.cursor()
    cursor.execute("SELECT * FROM PANEL_MEMBERS;")
    panel_name = cursor.fetchall()
    return render(request,'DEPARTMENT_PROJECT_MANAGEMENT_SYSTEM/panel_allotment.html',{'panel_allot': panel_name})


def add_panel_allot(request):
    if request.method=="POST":
        m=mysql.connector.connect(host="127.0.0.1",user="root",passwd="root",database='dept_project')
        cursor=m.cursor()
        d=request.POST
        for key,value in d.items():
            if key == 'panel_id':
                panel_id = d.get('panel_id')
            if key == 'usn':
                usn = d.get('usn')
        try:
            insert_str = "INSERT INTO PANEL_MEMBERS (PANEL_ID,USN) VALUES ('{}','{}')".format(panel_id,usn)
            cursor.execute(insert_str)
            m.commit()
            m.close()
            messages.success(request,"Details Entered Successfully!")
        except:
            messages.error(request,"Error")
            user_render = add_user_render(request)
            return user_render
    return panel_allot_render(request)
 
def panel_allot_render(request):
    m=sql.connect(host="127.0.0.1",user="root",passwd="root",database='dept_project')
    cursor = m.cursor()
    cursor.execute("SELECT USN FROM PANEL_MEMBERS;".format)
    usn_reg = cursor.fetchall()
    return render(request,'DEPARTMENT_PROJECT_MANAGEMENT_SYSTEM/add_panel_allot.html',{'name': usn_reg})

def error(request):
    return render(request,"DEPARTMENT_PROJECT_MANAGEMENT_SYSTEM/error.html")

def login_render(request):
    return render(request,"DEPARTMENT_PROJECT_MANAGEMENT_SYSTEM/login.html")

def student_form_render(request):
    return render(request,"DEPARTMENT_PROJECT_MANAGEMENT_SYSTEM/student_form.html")


def teacher_form_render(request):
    return render(request,"DEPARTMENT_PROJECT_MANAGEMENT_SYSTEM/guide_form.html")


def stud_dashboard_render(request):
    return render(request,"DEPARTMENT_PROJECT_MANAGEMENT_SYSTEM/demo.html")


def view_submissions(request):
    return render(request,"DEPARTMENT_PROJECT_MANAGEMENT_SYSTEM/stud_dashboard.html")

def guide_dashboard_render(request):
    return render(request,"DEPARTMENT_PROJECT_MANAGEMENT_SYSTEM/teacher_dashboard.html")


def view_checked_submissions(request):
    return render(request,"DEPARTMENT_PROJECT_MANAGEMENT_SYSTEM/teachers_dashboard.html")


def update_table_render(request):
    return render(request,"DEPARTMENT_PROJECT_MANAGEMENT_SYSTEM/update_student.html")
    
def update_student_details(request):
    m=mysql.connector.connect(host="127.0.0.1",user="root",passwd="root",database='dept_project')
    cursor = m.cursor()
    cursor.execute("SELECT * FROM STUDENT;")
    student_details = cursor.fetchall()
    return render(request,'DEPARTMENT_PROJECT_MANAGEMENT_SYSTEM/update_student.html',{'stud_details': student_details})
    
def update_student_update_table(request):
    student_details_render = render(request,"DEPARTMENT_PROJECT_MANAGEMENT_SYSTEM/update_student.html")
    if (student_details_render != None):
        table_render = update_student_details(request)
    return table_render