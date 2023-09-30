from django import forms
from django.contrib.auth.models import User
from . import models


#for admin
class AdminSigupForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']


#for student related form
class StudentUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
class StudentExtraForm(forms.ModelForm):
    class Meta:
        model=models.StudentExtra
        fields=['roll','cl','mobile','fee','status']



#for teacher related form
class TeacherUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
class TeacherExtraForm(forms.ModelForm):
    class Meta:
        model=models.TeacherExtra
        fields=['salary','mobile','status']




#for Attendance related form
presence_choices=(('Present','Present'),('Absent','Absent'))
class AttendanceForm(forms.Form):
    present_status=forms.ChoiceField( choices=presence_choices)
    date=forms.DateField()

class AskDateForm(forms.Form):
    date=forms.DateField()


#for notice related form
class NoticeForm(forms.ModelForm):
    class Meta:
        model=models.Notice
        fields='__all__'



#for contact us page
class ContactusForm(forms.Form):
    Name = forms.CharField(max_length=30)
    Email = forms.EmailField()
    Message = forms.CharField(max_length=500,widget=forms.Textarea(attrs={'rows': 3, 'cols': 30}))


from .models import Subject, TeacherExtra

class AssignTeacherToSubjectForm(forms.Form):
    predefined_subjects = [
        ('science', 'Science'),
        ('social', 'Social'),
        ('math', 'Math'),
        ('english', 'English'),
        ('nepali', 'Nepali'),
    ]

    subject = forms.ChoiceField(choices=predefined_subjects)
    teacher = forms.ModelChoiceField(queryset=TeacherExtra.objects.all())


from .models import TeacherExtra, classes


class AssignClassTeacherForm(forms.Form):
    teacher = forms.ModelChoiceField(queryset=TeacherExtra.objects.all(), label='Select Teacher')
    assigned_class = forms.ChoiceField(choices=classes, label='Select Class')


from .models import StudentExtra, Marks

class MarksForm(forms.ModelForm):
    student = forms.ModelChoiceField(queryset=StudentExtra.objects.all(), label="Student Name")
    
    class Meta:
        model = Marks
        fields = ['student', 'science', 'social', 'math', 'english', 'nepali']

