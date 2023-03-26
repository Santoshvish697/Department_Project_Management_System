from django.shortcuts import render,redirect,get_object_or_404
import mysql.connector as sql
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from dept_project.models import student_input,phase_allot,deliverable_project,diary,panel_members,users,guide,file_submit
from django.contrib import messages
import mysql.connector
from dept_project.forms import intern_details,SubmitForm

from django.db import connections
from dept_project.functions import handle_uploaded_file
import base64
from PIL import Image
import random
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail
from django.conf import settings

em=''
pwd=''
username = ''
login_obj = users()

def home(request):
    return render(request,"DEPARTMENT_PROJECT_MANAGEMENT_SYSTEM/index.html")
def login_redirect(request):
    return render(request,"DEPARTMENT_PROJECT_MANAGEMENT_SYSTEM/login.html")
    

# Create your views here.
def email(request,):
    if request.method == 'POST':
        message = request.POST['message']
        email = request.POST['email']
        name = request.POST['name']
        send_mail(
            name ,#title
            message, #message
            'settings.EMAIL_HOST_USER', #sender if not available considered the default
            [email], #receiver email
            fail_silently=False)
    return render(request, 'DEPARTMENT_PROJECT_MANAGEMENT_SYSTEM/email_integ.html')
    
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

def stud_username(request):
    global username
    m = mysql.connector.connect(host="127.0.0.1",user="root",passwd="root",database='dept_project')
    cursor = m.cursor()
    cursor.execute("SELECT FIRST_NAME FROM STUDENT WHERE EMAIL = '{}'".format(em))
    username = cursor.fetchall()
    return render(request,"DEPARTMENT_PROJECT_MANAGEMENT_SYSTEM/base_student_template.html",{'name' : username})


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
        return render(request,"DEPARTMENT_PROJECT_MANAGEMENT_SYSTEM/admin_login.html")

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
    cursor.execute("SELECT F.SUB_ID,F.USN,ST.FIRST_NAME,ST.LAST_NAME,F.PHASE_NO,SC.PHASE_DESC,T.SUB_STATUS,F.FILE FROM FILE_SUB AS F,STUDENT AS ST,TRANSACTIONS AS T,SCHEDULE AS SC,GUIDE AS G WHERE F.USN = ST.USN AND F.PHASE_NO = SC.PHASE_NO AND T.SUB_ID = F.SUB_ID AND G.USN = ST.USN AND G.EMAIL = 'amit@rvce.edu.in';;")
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
    cursor.execute("SELECT F.SUB_ID,F.PHASE_NO,SC.PHASE_DESC,E.RESULT FROM FILE_SUB AS F,SCHEDULE AS SC,TRANSACTIONS AS T,EVALUATE_RESULT AS E,STUDENT AS ST WHERE F.USN = ST.USN AND F.PHASE_NO = SC.PHASE_NO AND T.SUB_ID = F.SUB_ID AND E.SUB_ID = F.SUB_ID AND ST.EMAIL = '{}';".format(login_obj.email))
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


def internship_guide_render(request):
    m=sql.connect(host="127.0.0.1",user="root",passwd="root",database='dept_project')
    cursor = m.cursor()
    cursor.execute("SELECT * FROM INTERNSHIP_GUIDE;")
    intern_details = cursor.fetchall()
    return render(request,"DEPARTMENT_PROJECT_MANAGEMENT_SYSTEM/internship_guide_allotment.html",{'intern' : intern_details})

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

def panel_allot_render(request):
    m=sql.connect(host="127.0.0.1",user="root",passwd="root",database='dept_project')
    cursor = m.cursor()
    cursor.execute("SELECT USN FROM PANEL_MEMBERS;")
    usn_reg = cursor.fetchall()
    usn_lis = []
    for (title) in usn_reg:
        usn_lis.append(title[0])
    return render(request,'DEPARTMENT_PROJECT_MANAGEMENT_SYSTEM/add_panel_allot.html',{"usn_drop" : usn_lis})


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
            panel_allot_web_render = render(request,"DEPARTMENT_PROJECT_MANAGEMENT_SYSTEM/add_panel_allot.html")
            return panel_allot_web_render
    return panel_allot_render(request)
 

def error(request):
    return render(request,"DEPARTMENT_PROJECT_MANAGEMENT_SYSTEM/error.html")

def login_render(request):
    return render(request,"DEPARTMENT_PROJECT_MANAGEMENT_SYSTEM/login.html")

def student_form_render(request):
    return render(request,"DEPARTMENT_PROJECT_MANAGEMENT_SYSTEM/student_form.html")


def teacher_form_render(request):
    return render(request,"DEPARTMENT_PROJECT_MANAGEMENT_SYSTEM/guide_form.html")


def stud_dashboard_render(request):
    global username
    m = mysql.connector.connect(host="127.0.0.1",user="root",passwd="root",database='dept_project')
    cursor = m.cursor()
    cursor.execute("SELECT FIRST_NAME FROM STUDENT WHERE EMAIL = '{}'".format(em))
    username = cursor.fetchall()
    return render(request,"DEPARTMENT_PROJECT_MANAGEMENT_SYSTEM/demo.html",{'name' : username})



def username_render(request):
    global username
    m = mysql.connector.connect(host="127.0.0.1",user="root",passwd="root",database='dept_project')
    cursor = m.cursor()
    cursor.execute("SELECT FIRST_NAME FROM STUDENT WHERE EMAIL = '{}'".format(em))
    username = cursor.fetchall()
    return render(request,"DEPARTMENT_PROJECT_MANAGEMENT_SYSTEM/base_student_template.html",{'name' : username})

def upload_submission_render(request):
    return render(request,"DEPARTMENT_PROJECT_MANAGEMENT_SYSTEM/upload_submission.html")

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


def edit_student(request,id):
    m = mysql.connector.connect(host="127.0.0.1",user="root",passwd="root",database='dept_project')
    cursor = m.cursor()
    print(id)
    cursor.execute("SELECT FIRST_NAME,MIDDLE_NAME,LAST_NAME,PHONE_NO,USN FROM STUDENT WHERE USN = '{}';".format(id))
    student_details = cursor.fetchall()
    print(list(student_details))
    return render(request,"DEPARTMENT_PROJECT_MANAGEMENT_SYSTEM/update_student_form.html",{'student_render' : student_details})



def update_student(request):
    if request.method == "POST":
        print("YES")
        m=mysql.connector.connect(host="127.0.0.1",user="root",passwd="root",database='dept_project')
        cursor=m.cursor()
        d=request.POST
        for key,value in d.items():
            if key == 'usn_no':
                usn_no = d.get('usn_no')
                print(usn_no)
            if key == 'fname':
                first = d.get('fname')
                print(first)
            if key == 'mname':
                middle = d.get('mname')
                print(middle)
            if key == 'lname':
                last = d.get('lname')
                print(last)
            if key == 'phone':
                phone = d.get('phone')
                print(phone)
        try:
            print("Going to query")
            update_str = "UPDATE STUDENT SET FIRST_NAME = '{}',MIDDLE_NAME = '{}',LAST_NAME = '{}',PHONE_NO = '{}' WHERE USN = '{}';".format(first,middle,last,phone,usn_no)
            cursor.execute(update_str)
            print("Query Executed!")
            m.commit()
            m.close()
            messages.success(request,"Details Entered Successfully!")
            # redirect(update_student_update_table)
        except:
            messages.error(request,"Error")
    return render(request,"DEPARTMENT_PROJECT_MANAGEMENT_SYSTEM/update_student_form.html")

def delete_student(request,id):
    if request.method == "GET":
        m=mysql.connector.connect(host="127.0.0.1",user="root",passwd="root",database='dept_project')
        cursor=m.cursor()
        delete_str = "DELETE FROM STUDENT WHERE USN = '{}'".format(id)
        cursor.execute(delete_str)
        m.commit()
        m.close()
    delete_render = update_student_update_table(request)
    return delete_render

def edit_panel_allot(request,id):
    m = mysql.connector.connect(host="127.0.0.1",user="root",passwd="root",database='dept_project')
    cursor = m.cursor()
    print(id)
    cursor.execute("SELECT PANEL_ID,USN FROM PANEL_MEMBERS WHERE USN = '{}';".format(id))
    panel_details = cursor.fetchall()
    print(list(panel_details))
    return render(request,"DEPARTMENT_PROJECT_MANAGEMENT_SYSTEM/update_panel_allot.html",{'panel_allotment' : panel_details})

def panel_allot_update(request):
    if request.method == "POST":
        print("YES")
        m=mysql.connector.connect(host="127.0.0.1",user="root",passwd="root",database='dept_project')
        cursor=m.cursor()
        d=request.POST
        for key,value in d.items():
            if key == 'panel_id':
                pan_no = d.get('panel_id')
            if key == 'usn':
                usn_no = d.get('usn')
        try:
            panel_allot_str = "UPDATE STUDENT SET PANEL_ID = '{}' WHERE USN = '{}';".format(pan_no,usn_no)
            cursor.execute(panel_allot_str)
            m.commit()
            m.close()
            messages.success(request,"Details Entered Successfully!")
            # redirect(update_student_update_table)
        except:
            messages.error(request,"Error")
    return render(request,"DEPARTMENT_PROJECT_MANAGEMENT_SYSTEM/update_panel_allot.html")


def insert_intern(request):
    if request.method == "POST":
        forms = intern_details(request.POST)
        if forms.is_valid():
           try:
               forms.save()
               messages.success(request,"Data Inserted Successfully")
           except:
               messages.error(request,"Error!")
    forms = intern_details()
    return render(request,'DEPARTMENT_PROJECT_MANAGEMENT_SYSTEM/add_intern_allot.html',{'intern_form' : forms})





# def edit_intern_allot(request,id):
#     m = mysql.connector.connect(host="127.0.0.1",user="root",passwd="root",database='dept_project')
#     cursor = m.cursor()
#     cursor.execute("SELECT INTERN_ID,FIRST_NAME,MIDDLE_NAME,LAST_NAME,COMPANY,DOJ FROM INTERNSHIP_GUIDE WHERE INTERN_ID = {};".format(id))
#     intern_allot_details = cursor.fetchall()
#     print(list(intern_allot_details))
#     return render(request,"DEPARTMENT_PROJECT_MANAGEMENT_SYSTEM/update_intern_allot.html",{'intern_allot' : intern_allot_details})

# def intern_allot_update(request):
#     if request.method == "POST":
#         form = intern_details(request.POST)
#         m=mysql.connector.connect(host="127.0.0.1",user="root",passwd="root",database='dept_project')
#         cursor=m.cursor()
#         d=request.POST
#         for key,value in d.items():
#             if key == 'intern_id':
#                 intern_no = d.get('intern_id')
#             if key == 'fname':
#                 first = d.get('fname')
#             if key == 'mname':
#                 middle = d.get('mname')
#             if key == 'lname':
#                 last = d.get('lname')
#             if key == 'company':
#                 com = d.get('company')
#             if form.is_valid():
#                 my_date = form.cleaned_data['doj']
#                 my_model = intern_details(my_date= my_date)
                 
#         try:
#             intern_allot_str = "UPDATE INTERNSHIP_GUIDE SET INTERN_ID = {},FIRST_NAME = {},MIDDLE_NAME = {},LAST_NAME = {},COMPANY = {},DOJ = {};".format(intern_no,first,middle,last,com,doj)
#             cursor.execute(intern_allot_str)
#             m.commit()
#             m.close()
#             messages.success(request,"Details Entered Successfully!")
#             # redirect(update_student_update_table)
#         except:
#             messages.error(request,"Error")
#     return render(request,"DEPARTMENT_PROJECT_MANAGEMENT_SYSTEM/update_intern_allot.html")


def submission_render(request):
    if request.method == 'POST':
        submit = SubmitForm(request.POST,request.FILES)
        if submit.is_valid():
            try:
                handle_uploaded_file(request.FILES['file'])
                model_instance = submit.save(commit=False)
                model_instance.save()
                return HttpResponse("File Uploaded Successfully!")
            except:
                return HttpResponse("Error!")
    else:
        submit = SubmitForm()
    return render(request,"DEPARTMENT_PROJECT_MANAGEMENT_SYSTEM/add_submission.html",{'form' :submit })
    
from datetime import datetime

def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        binaryData = base64.base64encode(file)
    return binaryData
    
def submit_render(request):
    if request.method == 'POST':
            m = mysql.connector.connect(host="127.0.0.1",user="root",passwd="root",database='dept_project')
            cursor = m.cursor()
            submitted_at = datetime.today().strftime('%Y-%m-%d')
            print(submitted_at)
            d = request.POST
            for key,value in d.items():
                if key == 'usn_no':
                    usn = d.get('usn_no')
                    print(usn)
                if key == 'project_id':
                    id = d.get('project_id')
                if key == 'phase_no':
                    phase = d.get('phase_no')
                if key == 'file_submit':
                    file = d.get('file_submit')
                    print(file)
            file = convertToBinaryData(file)
            try:
                sql_insert_blob_query = "INSERT INTO STUDENT_SUB (USN, PROJECT_ID,SUBMITTED_AT,FILE_SUBMIT,PHASE_NO) VALUES ('{}','{}','{}',{},{})".format(usn,id,submitted_at,file,phase)
                cursor.execute(sql_insert_blob_query)
                m.commit()
                m.close()
                messages.success(request,"Updated record successfully!")
                return render(request,"DEPARTMENT_PROJECT_MANAGEMENT_SYSTEM/add_submission.html")
            except:
                messages.error(request,"Error") 
                return render(request,"DEPARTMENT_PROJECT_MANAGEMENT_SYSTEM/add_submission.html")
    return render(request,"DEPARTMENT_PROJECT_MANAGEMENT_SYSTEM/add_submission.html")

submission_obj = SubmitForm(instance=file_submit)

def upload_file(request):
    trans_id = 11004
    if request.method == 'POST':
        m = mysql.connector.connect(host="127.0.0.1",user="root",passwd="root",database='dept_project')
        cursor = m.cursor()
        form = SubmitForm(request.POST, request.FILES)
        if form.is_valid():
            try:
             print("File Valid")
             submission_obj = form.save(commit=False)
             messages.success(request,"Updated Record Successfully")
             submission_obj.save()
             sub_id = form.cleaned_data.get('sub_id')
             print(sub_id)
             trans_id = trans_id+1
             submitted_at = datetime.today().strftime('%Y-%m-%d')
             print(submitted_at)
             #INSERT INTO TRANSACTIONS VALUES  (11004,10042,'2023-03-21','ONTIME');
             sql_insert = "INSERT INTO TRANSACTIONS VALUES ({},{},'{}','{}');".format(trans_id,sub_id,submitted_at,'ONTIME')
             print(sql_insert)
             cursor.execute(sql_insert)
             m.commit()
             m.close()
             
            except:
             messages.error(request,"Failed to upload file")
    else:
        form = SubmitForm()
    return render(request, 'DEPARTMENT_PROJECT_MANAGEMENT_SYSTEM/add_submission.html', {'form': form})




def unchecked_table_render(request):
    m=sql.connect(host="127.0.0.1",user="root",passwd="root",database='dept_project')
    cursor=m.cursor()
    cursor.execute("SELECT F.SUB_ID,S.PHASE_NO,S.PHASE_DESC,T.SUBMITTED_AT FROM SCHEDULE AS S,TRANSACTIONS AS T,FILE_SUB AS F,PHASE_ALLOT AS PA, DELIVERABLE_PROJECT AS D WHERE S.PHASE_NO = F.PHASE_NO AND T.SUB_ID = PA.PHASE_ID AND F.USN = D.USN AND T.SUB_ID = F.SUB_ID AND F.EVAL = FALSE;")
    unchecked = cursor.fetchall()
    return render(request, 'DEPARTMENT_PROJECT_MANAGEMENT_SYSTEM/unchecked_view_assignment.html', {'unchecked_view_data': unchecked})


def unchecked_submit_view(request):
    unchecked_view_render = render(request,"DEPARTMENT_PROJECT_MANAGEMENT_SYSTEM/unchecked_view_assignment.html")
    if (unchecked_view_render != None):
        table_render = unchecked_table_render(request)
    return table_render

def edit_unchecked_submission(request,id):
    context = {}
    context["data"] = file_submit.objects.get(sub_id = id)
    return render(request,"DEPARTMENT_PROJECT_MANAGEMENT_SYSTEM/unchecked_view_form.html",context)

def update_file(request,id):
    files = file_submit.objects.get(sub_id = id)
    print(files.usn)
    if request.method == 'POST':
        form = SubmitForm(request.POST, request.FILES,instance=files)
        if form.is_valid():
            doc_file = request.FILES
            file_instance = file_submit(file=doc_file['file'],sub_id = id,usn = files.usn,phase_no = files.phase_no)
            print(file_instance)
            try:
             file_instance.save()
             messages.success(request,"Updated Successfully!")
            except:
                messages.error(request,"Error")
    else:
        form = SubmitForm(instance = files)
    return render(request, 'DEPARTMENT_PROJECT_MANAGEMENT_SYSTEM/unchecked_view_form.html', {'form': form})
 
 
def panel_project_render(request):
    m=sql.connect(host="127.0.0.1",user="root",passwd="root",database='dept_project')
    cursor = m.cursor()
    cursor.execute("SELECT PROJECT_ID,PROJECT_TITLE,PANEL_ID FROM DELIVERABLE_PROJECT;")
    panel_name = cursor.fetchall()
    return render(request,'DEPARTMENT_PROJECT_MANAGEMENT_SYSTEM/project_panel_allotment.html',{'panel_project_allot': panel_name})

  
def edit_project_panel_allot(request,id):
    m = mysql.connector.connect(host="127.0.0.1",user="root",passwd="root",database='dept_project')
    cursor = m.cursor()
    print(id)
    cursor.execute("SELECT PROJECT_ID,PROJECT_TITLE,PANEL_ID FROM DELIVERABLE_PROJECT WHERE PROJECT_ID = '{}';".format(id))
    panel_project_details = cursor.fetchall()
    print(list(panel_project_details))
    return render(request,"DEPARTMENT_PROJECT_MANAGEMENT_SYSTEM/update_project_allot.html",{'project_allotment' : panel_project_details})

def panel_project_update(request):
    if request.method == "POST":
        print("YES")
        m=mysql.connector.connect(host="127.0.0.1",user="root",passwd="root",database='dept_project')
        cursor=m.cursor()
        d=request.POST
        for key,value in d.items():
            if key == 'project_id':
                proj_no = d.get('project_id')
            if key == 'project_name':
                proj_title = d.get('project_name')
            if key == 'panel_id':
                panel_no = d.get('panel_id')
        try:
            panel_allot_str = "UPDATE DELIVERABLE_PROJECT SET PANEL_ID = {} WHERE PROJECT_ID = {};".format(proj_no,panel_no)
            cursor.execute(panel_allot_str)
            m.commit()
            m.close()
            messages.success(request,"Details Entered Successfully!")
            # redirect(update_student_update_table)
        except:
            messages.error(request,"Error")
    return render(request,"DEPARTMENT_PROJECT_MANAGEMENT_SYSTEM/update_project_allot.html")  


        
 
def guide_render(request):
    m=sql.connect(host="127.0.0.1",user="root",passwd="root",database='dept_project')
    cursor = m.cursor()
    cursor.execute("SELECT GUIDE_ID,FIRST_NAME,MIDDLE_NAME,LAST_NAME,EMAIL,PHONE_NO,USN FROM GUIDE;")
    guide_details = cursor.fetchall()
    return render(request,'DEPARTMENT_PROJECT_MANAGEMENT_SYSTEM/guide_detail.html',{'guide_detail': guide_details})

  
def edit_guide(request,id):
    m = mysql.connector.connect(host="127.0.0.1",user="root",passwd="root",database='dept_project')
    cursor = m.cursor()
    print(id)
    cursor.execute("SELECT GUIDE_ID,FIRST_NAME,MIDDLE_NAME,LAST_NAME,EMAIL,PHONE_NO,PROJECT_ID,USN FROM GUIDE WHERE GUIDE_ID = {};".format(id))
    guide_details = cursor.fetchall()
    return render(request,"DEPARTMENT_PROJECT_MANAGEMENT_SYSTEM/guide_update.html",{'guide_update' : guide_details})

def guide_add_render(request):
    if request.method == "POST":
        print("YES")
        m=mysql.connector.connect(host="127.0.0.1",user="root",passwd="root",database='dept_project')
        cursor=m.cursor()
        d=request.POST
        for key,value in d.items():
            if key == 'guide_id':
                id = d.get('guide_id')
            if key == 'fname':
                first = d.get('fname')
            if key == 'fname':
                middle = d.get('mname')
            if key == 'lname':
                last = d.get('lname')
            if key == 'email':
                email = d.get('email')
            if key == 'phone':
                phone_no = d.get('phone')
            if key== 'project_id':
                project_id = d.get('project_id')
            if key == 'usn':
                usn_no = d.get('usn')
        try:
            guide_str = "INSERT INTO GUIDE VALUES ('{}','{}','{}','{}','{}','{}',{},'{}')".format(id,first,middle,last,key,email,phone_no,project_id,usn_no)
            cursor.execute(guide_str)
            m.commit()
            m.close()
            messages.success(request,"Details Entered Successfully!")
            # redirect(update_student_update_table)
        except:
            messages.error(request,"Error")
    return render(request,"DEPARTMENT_PROJECT_MANAGEMENT_SYSTEM/add_guide.html")  

def unchecked_submissions_render(request):
    m=sql.connect(host="127.0.0.1",user="root",passwd="root",database='dept_project')
    cursor=m.cursor()
    cursor.execute("SELECT F.USN,ST.FIRST_NAME,ST.LAST_NAME,F.PHASE_NO,SC.PHASE_DESC,T.SUB_STATUS FROM FILE_SUB AS F,STUDENT AS ST,TRANSACTIONS AS T,SCHEDULE AS SC,GUIDE AS G WHERE F.USN = ST.USN AND F.PHASE_NO = SC.PHASE_NO AND T.SUB_ID = F.SUB_ID AND G.USN = ST.USN AND G.EMAIL = 'amit@rvce.edu.in';")
    unchecked = cursor.fetchall()
    return render(request, 'DEPARTMENT_PROJECT_MANAGEMENT_SYSTEM/unchecked_view_assignment.html', {'unchecked_view_data': unchecked})


def edit_marks_allot(request,id):
    m = mysql.connector.connect(host="127.0.0.1",user="root",passwd="root",database='dept_project')
    cursor = m.cursor()
    print(id)
    cursor.execute("SELECT F.SUB_ID FROM FILE_SUB AS F WHERE F.SUB_ID = {}".format(id))
    sub_id = cursor.fetchall()
    print(list(sub_id))
    return render(request,"DEPARTMENT_PROJECT_MANAGEMENT_SYSTEM/add_result.html",{'id' : sub_id})
guide_id = '1200'
def marks_allot_update(request,id):
        global guide_id
        if request.method == "GET":
         m = mysql.connector.connect(host="127.0.0.1",user="root",passwd="root",database='dept_project')
         cursor = m.cursor()
         select_query = "SELECT DISTINCT GUIDE_ID FROM GUIDE AS G, DELIVERABLE_PROJECT AS D, STUDENT AS S, FILE_SUB AS F WHERE G.PROJECT_ID = D.PROJECT_ID AND G.USN = F.USN AND G.USN = S.USN AND F.SUB_ID = {};".format(id)
         cursor.execute(select_query)
         guide_id = list(cursor.fetchall())[0][0]
         cursor.execute("SELECT F.SUB_ID FROM FILE_SUB AS F WHERE F.SUB_ID = {}".format(id))
         sub_id = cursor.fetchall()
        #  print(list(sub_id))
         return render(request,"DEPARTMENT_PROJECT_MANAGEMENT_SYSTEM/add_result.html",{'id' : sub_id})   
        elif request.method == "POST":
         m=mysql.connector.connect(host="127.0.0.1",user="root",passwd="root",database='dept_project')
         cursor=m.cursor()
         d=request.POST
         for key,value in d.items():
            if key == 'sub_id':
                 id = d.get('sub_id')
            if key == 'usn':
                usn_no = d.get('usn')
            if key == 'rubric_1_marks':
                rub_1 = d.get('rubric_1_marks')
            if key == 'rubric_1_marks':
                rub_2 = d.get('rubric_2_marks')
            if key == 'rubric_1_marks':
                rub_3 = d.get('rubric_3_marks')
         try:
          avg = rub_1 + rub_2 + rub_3
          panel_allot_str = "INSERT INTO EVALUATE_RESULT VALUES ({},'{}',{},{},{},'{}',{});".format(id,usn_no,rub_1,rub_2,rub_3,guide_id,avg)
          cursor.execute(panel_allot_str)
          update_str = "UPDATE FILE_SUB SET EVAL = TRUE WHERE SUB_ID = '{}'".format(id)
          m.commit()
          m.close()
          messages.success(request,"Details Entered Successfully!")   # redirect(update_student_update_table)
         except:
            messages.error(request,"Error")
        return assign_marks_render(request) 

def assign_marks_render(request):
    return render(request,"DEPARTMENT_PROJECT_MANAGEMENT_SYSTEM/add_result.html")