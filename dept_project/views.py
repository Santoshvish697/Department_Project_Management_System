from django.shortcuts import render
import mysql.connector as sql
from django.contrib import messages
em=''
pwd=''
# Create your views here.
def loginaction(request):
    global em,pwd
    if request.method=="POST":
        m=sql.connect(host="127.0.0.1",user="root",passwd="root",database='department_project_mgmt')
        cursor=m.cursor()
        d=request.POST
        for key,value in d.items():
            if key=="email":
                em=value
            if key=="password":
                pwd=value
        print(em)
        c="select * from USERS where EMAIL = '{}' and PASSWORD ='{}'".format(em,pwd)
        print(c)
        cursor.execute(c)
        t=tuple(cursor.fetchall())
        if t==():
            messages.info(request, 'Invalid Credentials')
            # error_render = error(request)
            # return error_render
        else:
            dashboard_render = stud_dashboard(request)
            return dashboard_render

    return login_render(request)


def stud_dashboard(request):
    return render(request,"DEPARTMENT_PROJECT_MANAGEMENT_SYSTEM/stud_dashboard.html")


def error(request):
    return render(request,"DEPARTMENT_PROJECT_MANAGEMENT_SYSTEM/error.html")

def login_render(request):
    return render(request,"DEPARTMENT_PROJECT_MANAGEMENT_SYSTEM/login.html")