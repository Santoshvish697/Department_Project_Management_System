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
    email = models.CharField(max_length=25)
    Phone_no = models.CharField(max_length=15,default=0000000000)

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
        
class schedule(models.Model):
    phase_no = models.IntegerField(primary_key=True)
    phase_desc = models.CharField(max_length=100)
    due_date = models.DateField()
    
    class Meta:
        db_table = 'SCHEDULE'
    
class phase_allot(models.Model):
    phase_ID = models.IntegerField(primary_key=True)
    Project_ID = models.ForeignKey(deliverable_project,on_delete=models.CASCADE)
    phase_no = models.ForeignKey(schedule,on_delete = models.CASCADE,default = 0)
    due_date = models.DateField()
    late_submission = models.IntegerField()
    class Meta:
        db_table = 'PHASE_ALLOT'

class file_submit(models.Model):
    sub_id = models.IntegerField(primary_key=True,default = 100)
    usn = models.CharField(max_length=25,default= "1RV20IS000")
    phase_no = models.IntegerField(default = 1) 
    file = models.FileField(upload_to="dept_project/static/DEPARTMENT_PROJECT_MANAGEMENT_SYSTEM/upload/") 
    eval = models.BooleanField(default=False)
    class Meta:
        db_table = 'FILE_SUB'
    
class guide(models.Model):
    Guide_ID = models.IntegerField(primary_key=True)
    fname = models.CharField(max_length=25)
    mname = models.CharField(max_length=25)
    lname = models.CharField(max_length=25)
    Phone_No = models.CharField(max_length=15,default=0000000000)
    email = models.ForeignKey(users,on_delete = models.CASCADE)
    project_ID = models.ForeignKey(deliverable_project,blank = True, null = True,on_delete=models.SET_NULL)
    usn = models.ForeignKey(student_input,blank = True, null = True,on_delete=models.SET_NULL)
    class Meta:
        db_table = 'GUIDE'


class coordinator(models.Model):
    dept_name = models.CharField(max_length=25)
    email = models.ForeignKey(users,null = True,on_delete = models.CASCADE)
    class Meta:
        db_table = 'COORDINATOR'



class internship_guide(models.Model):
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
    class Meta:
        db_table = 'PANEL_ALLOT'

   
class EvaluateResult(models.Model):
    sub_id = models.IntegerField(default = 0)  #foreign key attribute
    
    usn = models.CharField(max_length = 25,default = "1RV20IS000")
    # subject_exam_marks=models.FloatField(default=0)
    rubric_1_marks = models.IntegerField(default=0)
    rubric_2_marks = models.IntegerField(default=0)
    rubric_3_marks = models.IntegerField(default=0)
    result = models.IntegerField(default=0)
    guide_no = models.CharField(default = '1200',max_length=25)