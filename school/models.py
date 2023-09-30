from django.db import models
from django.contrib.auth.models import User
# Create your models here.

classes=[('one','one'),('two','two'),('three','three'),
('four','four'),('five','five'),('six','six'),('seven','seven'),('eight','eight'),('nine','nine'),('ten','ten')]

class TeacherExtra(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    salary = models.PositiveIntegerField(null=False)
    joindate=models.DateField(auto_now_add=True)
    mobile = models.CharField(max_length=40)
    status=models.BooleanField(default=False)
    assigned_class = models.CharField(max_length=10, choices=classes, blank=True)
    def __str__(self):
        return self.user.first_name
    @property
    def get_id(self):
        return self.user.id
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name



class StudentExtra(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    roll = models.CharField(max_length=10)
    mobile = models.CharField(max_length=40,null=True)
    fee=models.PositiveIntegerField(null=True)
    cl= models.CharField(max_length=10,choices=classes,default='one')
    status=models.BooleanField(default=False)

    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return self.user.first_name



class Attendance(models.Model):
    roll=models.CharField(max_length=10,null=True)
    date=models.DateField()
    cl=models.CharField(max_length=10)
    present_status = models.CharField(max_length=10)



class Notice(models.Model):
    date=models.DateField(auto_now=True)
    by=models.CharField(max_length=20,null=True,default='school')
    message=models.CharField(max_length=500)

    

from .models import TeacherExtra

class Subject(models.Model):
    name = models.CharField(max_length=100)
    teacher = models.ForeignKey(TeacherExtra, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name
    
from functools import wraps
from django.shortcuts import redirect

def class_teacher_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Check if the user is a class teacher
        if request.user.teacherextra.assigned_class:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('teacher_dashboard')  # Redirect if not a class teacher
    return _wrapped_view

from school.models import StudentExtra


class Marks(models.Model):
    student = models.ForeignKey(StudentExtra, on_delete=models.CASCADE)
    science = models.DecimalField(max_digits=5, decimal_places=2)
    social = models.DecimalField(max_digits=5, decimal_places=2)
    math = models.DecimalField(max_digits=5, decimal_places=2)
    english = models.DecimalField(max_digits=5, decimal_places=2)
    nepali = models.DecimalField(max_digits=5, decimal_places=2)


    def __str__(self):
        return f"{self.student.get_name()} - {self.subject}"

