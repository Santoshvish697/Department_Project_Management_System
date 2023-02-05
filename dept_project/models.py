from django.db import models


class users(models.Model):
    email = models.CharField(max_length=50,primary_key=True)
    pwd = models.CharField(max_length=50)
    class Meta:
        db_table = 'USERS'


class student_input(models.Model):
    usn = models.CharField(max_length=25,primary_key=True)
    fname = models.CharField(max_length=25)
    mname = models.CharField(max_length=25)
    lname = models.CharField(max_length=25)
    email = models.ForeignKey(users,on_delete=models.CASCADE)
    phone_no = models.CharField(max_length=15)
    class Meta:
        db_table="STUDENT"

class panel_members(models.Model):
    panel_id = models.IntegerField(primary_key=True)
    usn = models.CharField(max_length=25)
    class Meta:
        db_table = 'PANEL_MEMBERS'

class deliverable_project(models.Model):
    project_ID = models.IntegerField(primary_key=True)
    Project_Title = models.CharField(max_length=50)
    Project_Objective = models.CharField(max_length=150)
    Project_Outcome = models.CharField(max_length=150)
    project_Domain = models.CharField(max_length=100)
    panel_ID = models.IntegerField(panel_members)
    usn = models.ForeignKey(student_input,null=True,on_delete=models.SET_NULL)
    class Meta:
        db_table = 'DELIVERABLE_PROJECT'


class diary(models.Model):
    diary_id = models.IntegerField(primary_key=True)
    date= models.DateField()
    comments = models.CharField(max_length=100)
    work_done = models.CharField(max_length=100)
    usn = models.ForeignKey(student_input,on_delete=models.CASCADE)
    class Meta:
        db_table = 'DIARY'


class phase_allot(models.Model):
    phase_ID = models.IntegerField(primary_key=True)
    Project_ID = models.ForeignKey(deliverable_project,on_delete=models.CASCADE)
    phase_no = models.IntegerField()
    due_date = models.DateField()
    late_submission = models.IntegerField()
    class Meta:
        db_table = 'PHASE_ALLOT'

class guide(models.Model):
    Guide_ID = models.IntegerField(primary_key=True)
    fname = models.CharField(max_length=25)
    mname = models.CharField(max_length=25)
    lname = models.CharField(max_length=25)
    phone_no = models.CharField(max_length=15)
    email = models.ForeignKey(users,on_delete = models.CASCADE)
    project_ID = models.ForeignKey(deliverable_project,blank = True, null = True,on_delete=models.SET_NULL)
    usn = models.ForeignKey(student_input,blank = True, null = True,on_delete=models.SET_NULL)
    id = models.ForeignKey(diary,blank = True, null = True,on_delete=models.SET_NULL)
    class Meta:
        db_table = 'GUIDE'


# class coordinator(models.Model):
#     dept_name = models.CharField(max_length=25)
#     panel_ID = models.ForeignKey(panel_members,blank = True,null = True,on_delete=models.SET_NULL)
#     usn = models.ForeignKey(student_input,null = True,on_delete=models.SET_NULL)
#     email = models.ForeignKey(users,null = True,on_delete = models.CASCADE)
#     id = models.ForeignKey(guide,null = True,on_delete = models.SET_NULL)
#     usn = models.ForeignKey(student_input,on_delete=models.SET_NULL)
#     class Meta:
#         db_table = 'COORDINATOR'



class internship_guide():
    intern_ID = models.IntegerField(primary_key=True)
    fname = models.CharField(max_length=25)
    mname = models.CharField(max_length=25)
    lname = models.CharField(max_length=25)
    company = models.CharField(max_length=25)
    doj = models.DateField()
    class Meta:
        db_table = 'INTERNSHIP_GUIDE'


class panel_allot(models.Model):
    allot_num = models.AutoField(primary_key=True)
    guide_ID = models.ForeignKey(guide,on_delete=models.CASCADE)
    panel_ID = models.ForeignKey(panel_members,on_delete=models.CASCADE)

    

'''
CREATE TABLE COORDINATOR (
Department_Name VARCHAR(25) PRIMARY KEY,
Panel_ID INT(11),
ID VARCHAR(25),
USN VARCHAR(25),
Email VARCHAR(25),
FOREIGN KEY (Email) REFERENCES USERS(Email) ON DELETE CASCADE,	
FOREIGN KEY (ID) REFERENCES GUIDE(Guide_ID) ON DELETE SET NULL,
FOREIGN KEY (USN) REFERENCES STUDENT(USN),
FOREIGN KEY (Panel_ID) REFERENCES PANEL_MEMBERS(Panel_ID)
);
'''


    
