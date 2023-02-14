from datetime import datetime
from django import forms
from dept_project.models import internship_guide,file_submit

class intern_details(forms.ModelForm):
    intern_ID = forms.CharField(widget=forms.TextInput)
    fname = forms.CharField(widget=forms.TextInput)
    mname = forms.CharField(widget=forms.TextInput)
    lname = forms.CharField(widget=forms.TextInput)
    doj = forms.DateField(widget=forms.DateInput)

    class Meta:
        model = internship_guide
        fields = "__all__"
    # class Meta:
    #     model = internship_guide
    #     fields = ['doj']
    # def clean_my_date(self):
    #     date = self.cleaned_data['my_date']
    #     return datetime.strptime(date, '%Y-%m-%d').date()  
    
class SubmitForm(forms.ModelForm): 
    sub_id = forms.IntegerField(min_value=1000) 
    class Meta:  
        model = file_submit
        fields = ['sub_id','usn','phase_no','file']
        
                  
    
