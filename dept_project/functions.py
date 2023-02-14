def handle_uploaded_file(f):  
    with open('dept_project/static/DEPARTMENT_PROJECT_MANAGEMENT_SYSTEM/upload/'+f.name, 'wb+') as destination:  
        for chunk in f.chunks():  
            destination.write(chunk) 