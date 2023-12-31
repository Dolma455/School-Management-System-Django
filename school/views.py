from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from django.core.mail import send_mail

def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'school/index.html')



#for showing signup/login button for teacher
def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'school/adminclick.html')


#for showing signup/login button for teacher
def teacherclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'school/teacherclick.html')


#for showing signup/login button for student
def studentclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'school/studentclick.html')





def admin_signup_view(request):
    form=forms.AdminSigupForm()
    if request.method=='POST':
        form=forms.AdminSigupForm(request.POST)
        if form.is_valid():
            user=form.save()
            user.set_password(user.password)
            user.save()


            my_admin_group = Group.objects.get_or_create(name='ADMIN')
            my_admin_group[0].user_set.add(user)

            return HttpResponseRedirect('adminlogin')
    return render(request,'school/adminsignup.html',{'form':form})




def student_signup_view(request):
    form1=forms.StudentUserForm()
    form2=forms.StudentExtraForm()
    mydict={'form1':form1,'form2':form2}
    if request.method=='POST':
        form1=forms.StudentUserForm(request.POST)
        form2=forms.StudentExtraForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            user=form1.save()
            user.set_password(user.password)
            user.save()
            f2=form2.save(commit=False)
            f2.user=user
            user2=f2.save()

            my_student_group = Group.objects.get_or_create(name='STUDENT')
            my_student_group[0].user_set.add(user)

        return HttpResponseRedirect('studentlogin')
    return render(request,'school/studentsignup.html',context=mydict)


def teacher_signup_view(request):
    form1=forms.TeacherUserForm()
    form2=forms.TeacherExtraForm()
    mydict={'form1':form1,'form2':form2}
    if request.method=='POST':
        form1=forms.TeacherUserForm(request.POST)
        form2=forms.TeacherExtraForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            user=form1.save()
            user.set_password(user.password)
            user.save()
            f2=form2.save(commit=False)
            f2.user=user
            user2=f2.save()

            my_teacher_group = Group.objects.get_or_create(name='TEACHER')
            my_teacher_group[0].user_set.add(user)

        return HttpResponseRedirect('teacherlogin')
    return render(request,'school/teachersignup.html',context=mydict)






#for checking user is techer , student or admin
def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()
def is_teacher(user):
    return user.groups.filter(name='TEACHER').exists()
def is_student(user):
    return user.groups.filter(name='STUDENT').exists()


def afterlogin_view(request):
    if is_admin(request.user):
        return redirect('admin-dashboard')
    elif is_teacher(request.user):
        accountapproval=models.TeacherExtra.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            return redirect('teacher-dashboard')
        else:
            return render(request,'school/teacher_wait_for_approval.html')
    elif is_student(request.user):
        accountapproval=models.StudentExtra.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            return redirect('student-dashboard')
        else:
            return render(request,'school/student_wait_for_approval.html')




#for dashboard of adminnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_dashboard_view(request):
    teachercount=models.TeacherExtra.objects.all().filter(status=True).count()
    pendingteachercount=models.TeacherExtra.objects.all().filter(status=False).count()

    studentcount=models.StudentExtra.objects.all().filter(status=True).count()
    pendingstudentcount=models.StudentExtra.objects.all().filter(status=False).count()

    teachersalary=models.TeacherExtra.objects.filter(status=True).aggregate(Sum('salary'))
    pendingteachersalary=models.TeacherExtra.objects.filter(status=False).aggregate(Sum('salary'))

    studentfee=models.StudentExtra.objects.filter(status=True).aggregate(Sum('fee',default=0))
    pendingstudentfee=models.StudentExtra.objects.filter(status=False).aggregate(Sum('fee'))

    notice=models.Notice.objects.all()

    #aggregate function return dictionary so fetch data from dictionay
    mydict={
        'teachercount':teachercount,
        'pendingteachercount':pendingteachercount,

        'studentcount':studentcount,
        'pendingstudentcount':pendingstudentcount,

        'teachersalary':teachersalary['salary__sum'],
        'pendingteachersalary':pendingteachersalary['salary__sum'],

        'studentfee':studentfee['fee__sum'],
        'pendingstudentfee':pendingstudentfee['fee__sum'],

        'notice':notice

    }

    return render(request,'school/admin_dashboard.html',context=mydict)







#for teacher sectionnnnnnnn by admin

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_teacher_view(request):
    return render(request,'school/admin_teacher.html')

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_teacher_view(request):
    form1=forms.TeacherUserForm()
    form2=forms.TeacherExtraForm()
    mydict={'form1':form1,'form2':form2}
    if request.method=='POST':
        form1=forms.TeacherUserForm(request.POST)
        form2=forms.TeacherExtraForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            user=form1.save()
            user.set_password(user.password)
            user.save()

            f2=form2.save(commit=False)
            f2.user=user
            f2.status=True
            f2.save()

            my_teacher_group = Group.objects.get_or_create(name='TEACHER')
            my_teacher_group[0].user_set.add(user)

        return HttpResponseRedirect('admin-teacher')
    return render(request,'school/admin_add_teacher.html',context=mydict)


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_teacher_view(request):
    teachers=models.TeacherExtra.objects.all().filter(status=True)
    return render(request,'school/admin_view_teacher.html',{'teachers':teachers})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_approve_teacher_view(request):
    teachers=models.TeacherExtra.objects.all().filter(status=False)
    return render(request,'school/admin_approve_teacher.html',{'teachers':teachers})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def approve_teacher_view(request,pk):
    teacher=models.TeacherExtra.objects.get(id=pk)
    teacher.status=True
    teacher.save()
    return redirect(reverse('admin-approve-teacher'))


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_teacher_view(request,pk):
    teacher=models.TeacherExtra.objects.get(id=pk)
    user=models.User.objects.get(id=teacher.user_id)
    user.delete()
    teacher.delete()
    return redirect('admin-approve-teacher')


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_teacher_from_school_view(request,pk):
    teacher=models.TeacherExtra.objects.get(id=pk)
    user=models.User.objects.get(id=teacher.user_id)
    user.delete()
    teacher.delete()
    return redirect('admin-view-teacher')


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def update_teacher_view(request,pk):
    teacher=models.TeacherExtra.objects.get(id=pk)
    user=models.User.objects.get(id=teacher.user_id)

    form1=forms.TeacherUserForm(instance=user)
    form2=forms.TeacherExtraForm(instance=teacher)
    mydict={'form1':form1,'form2':form2}

    if request.method=='POST':
        form1=forms.TeacherUserForm(request.POST,instance=user)
        form2=forms.TeacherExtraForm(request.POST,instance=teacher)
        print(form1)
        if form1.is_valid() and form2.is_valid():
            user=form1.save()
            user.set_password(user.password)
            user.save()
            f2=form2.save(commit=False)
            f2.status=True
            f2.save()
            return redirect('admin-view-teacher')
    return render(request,'school/admin_update_teacher.html',context=mydict)


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_teacher_salary_view(request):
    teachers=models.TeacherExtra.objects.all()
    return render(request,'school/admin_view_teacher_salary.html',{'teachers':teachers})






#for student by admin
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_student_view(request):
    return render(request,'school/admin_student.html')


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_student_view(request):
    form1=forms.StudentUserForm()
    form2=forms.StudentExtraForm()
    mydict={'form1':form1,'form2':form2}
    if request.method=='POST':
        form1=forms.StudentUserForm(request.POST)
        form2=forms.StudentExtraForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            print("form is valid")
            user=form1.save()
            user.set_password(user.password)
            user.save()

            f2=form2.save(commit=False)
            f2.user=user
            f2.status=True
            f2.save()

            my_student_group = Group.objects.get_or_create(name='STUDENT')
            my_student_group[0].user_set.add(user)
        else:
            print("form is invalid")
        return HttpResponseRedirect('admin-student')
    return render(request,'school/admin_add_student.html',context=mydict)


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_student_view(request):
    students=models.StudentExtra.objects.all().filter(status=True)
    return render(request,'school/admin_view_student.html',{'students':students})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_student_from_school_view(request,pk):
    student=models.StudentExtra.objects.get(id=pk)
    user=models.User.objects.get(id=student.user_id)
    user.delete()
    student.delete()
    return redirect('admin-view-student')


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_student_view(request,pk):
    student=models.StudentExtra.objects.get(id=pk)
    user=models.User.objects.get(id=student.user_id)
    user.delete()
    student.delete()
    return redirect('admin-approve-student')


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def update_student_view(request,pk):
    student=models.StudentExtra.objects.get(id=pk)
    user=models.User.objects.get(id=student.user_id)
    form1=forms.StudentUserForm(instance=user)
    form2=forms.StudentExtraForm(instance=student)
    mydict={'form1':form1,'form2':form2}
    if request.method=='POST':
        form1=forms.StudentUserForm(request.POST,instance=user)
        form2=forms.StudentExtraForm(request.POST,instance=student)
        print(form1)
        if form1.is_valid() and form2.is_valid():
            user=form1.save()
            user.set_password(user.password)
            user.save()
            f2=form2.save(commit=False)
            f2.status=True
            f2.save()
            return redirect('admin-view-student')
    return render(request,'school/admin_update_student.html',context=mydict)



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_approve_student_view(request):
    students=models.StudentExtra.objects.all().filter(status=False)
    return render(request,'school/admin_approve_student.html',{'students':students})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def approve_student_view(request,pk):
    students=models.StudentExtra.objects.get(id=pk)
    students.status=True
    students.save()
    return redirect(reverse('admin-approve-student'))


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_student_fee_view(request):
    students=models.StudentExtra.objects.all()
    return render(request,'school/admin_view_student_fee.html',{'students':students})






#attendance related view
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_attendance_view(request):
    return render(request,'school/admin_attendance.html')


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_take_attendance_view(request,cl):
    students=models.StudentExtra.objects.all().filter(cl=cl)
    print(students)
    aform=forms.AttendanceForm()
    if request.method=='POST':
        form=forms.AttendanceForm(request.POST)
        if form.is_valid():
            Attendances=request.POST.getlist('present_status')
            date=form.cleaned_data['date']
            for i in range(len(Attendances)):
                AttendanceModel=models.Attendance()
                AttendanceModel.cl=cl
                AttendanceModel.date=date
                AttendanceModel.present_status=Attendances[i]
                AttendanceModel.roll=students[i].roll
                AttendanceModel.save()
            return redirect('admin-attendance')
        else:
            print('form invalid')
    return render(request,'school/admin_take_attendance.html',{'students':students,'aform':aform})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_attendance_view(request, cl):
    form = forms.AskMonthForm()  # Instantiate the form
    if request.method == 'POST':
        form = forms.AskMonthForm(request.POST)
        if form.is_valid():
            year = form.cleaned_data['year']
            month = form.cleaned_data['month']

            # Get all students in the class
            students = models.StudentExtra.objects.filter(cl=cl)

            # Prepare data for the template
            data = []
            for student in students:
                # Get the attendance records for the student for the specified month
                attendance_records = models.Attendance.objects.filter(date__year=year, date__month=month, cl=cl, roll=student.roll)

                data.append({
                    'student': student,
                    'attendance_records': attendance_records,
                })

            return render(request, 'school/admin_view_attendance_page.html', {'cl': cl, 'data': data, 'year': year, 'month': month})
    return render(request, 'school/admin_view_attendance_ask_month.html', {'cl': cl, 'form': form})

#fee related view by admin
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_fee_view(request):
    return render(request,'school/admin_fee.html')


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_fee_view(request,cl):
    feedetails=models.StudentExtra.objects.all().filter(cl=cl)
    return render(request,'school/admin_view_fee.html',{'feedetails':feedetails,'cl':cl})


#notice related viewss
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_notice_view(request):
    form=forms.NoticeForm()
    if request.method=='POST':
        form=forms.NoticeForm(request.POST)
        if form.is_valid():
            form=form.save(commit=False)
            form.by=request.user.first_name
            form.save()
            return redirect('admin-dashboard')
    return render(request,'school/admin_notice.html',{'form':form})



#for TEACHER  LOGIN    SECTION
@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_dashboard_view(request):
    teacherdata=models.TeacherExtra.objects.all().filter(status=True,user_id=request.user.id)
    notice=models.Notice.objects.all()
    mydict={
        'salary':teacherdata[0].salary,
        'mobile':teacherdata[0].mobile,
        'date':teacherdata[0].joindate,
        'notice':notice
    }
    return render(request,'school/teacher_dashboard.html',context=mydict)



@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_attendance_view(request):
    return render(request,'school/teacher_attendance.html')


@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_take_attendance_view(request,cl):
    students=models.StudentExtra.objects.all().filter(cl=cl)
    aform=forms.AttendanceForm()
    if request.method=='POST':
        form=forms.AttendanceForm(request.POST)
        if form.is_valid():
            Attendances=request.POST.getlist('present_status')
            date=form.cleaned_data['date']
            for i in range(len(Attendances)):
                AttendanceModel=models.Attendance()
                AttendanceModel.cl=cl
                AttendanceModel.date=date
                AttendanceModel.present_status=Attendances[i]
                AttendanceModel.roll=students[i].roll
                AttendanceModel.save()
            return redirect('teacher-attendance')
        else:
            print('form invalid')
    return render(request,'school/teacher_take_attendance.html',{'students':students,'aform':aform})


@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_view_attendance_view(request,cl):
    form=forms.AskDateForm()
    if request.method=='POST':
        form=forms.AskDateForm(request.POST)
        if form.is_valid():
            date=form.cleaned_data['date']
            attendancedata=models.Attendance.objects.all().filter(date=date,cl=cl)
            studentdata=models.StudentExtra.objects.all().filter(cl=cl)
            mylist=zip(attendancedata,studentdata)
            return render(request,'school/teacher_view_attendance_page.html',{'cl':cl,'mylist':mylist,'date':date})
        else:
            print('form invalid')
    return render(request,'school/teacher_view_attendance_ask_date.html',{'cl':cl,'form':form})


@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_notice_view(request):
    form=forms.NoticeForm()
    if request.method=='POST':
        form=forms.NoticeForm(request.POST)
        if form.is_valid():
            form=form.save(commit=False)
            form.by=request.user.first_name
            form.save()
            return redirect('teacher-dashboard')
        else:
            print('form invalid')
    return render(request,'school/teacher_notice.html',{'form':form})


#FOR STUDENT AFTER THEIR Login
@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_dashboard_view(request):
    studentdata=models.StudentExtra.objects.all().filter(status=True,user_id=request.user.id)
    notice=models.Notice.objects.all()
    mydict={
        'roll':studentdata[0].roll,
        'mobile':studentdata[0].mobile,
        'fee':studentdata[0].fee,
        'notice':notice
    }
    return render(request,'school/student_dashboard.html',context=mydict)



@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_attendance_view(request):
    form=forms.AskDateForm()
    if request.method=='POST':
        form=forms.AskDateForm(request.POST)
        if form.is_valid():
            date=form.cleaned_data['date']
            studentdata=models.StudentExtra.objects.all().filter(user_id=request.user.id,status=True)
            attendancedata=models.Attendance.objects.all().filter(date=date,cl=studentdata[0].cl,roll=studentdata[0].roll)
            mylist=zip(attendancedata,studentdata)
            return render(request,'school/student_view_attendance_page.html',{'mylist':mylist,'date':date})
        else:
            print('form invalid')
    return render(request,'school/student_view_attendance_ask_date.html',{'form':form})



# for aboutus and contact us
def aboutus_view(request):
    return render(request,'school/aboutus.html')

def contactus_view(request):
    sub = forms.ContactusForm()
    if request.method == 'POST':
        sub = forms.ContactusForm(request.POST)
        if sub.is_valid():
            email = sub.cleaned_data['Email']
            name=sub.cleaned_data['Name']
            message = sub.cleaned_data['Message']
            send_mail(str(name)+' || '+str(email),message,settings.EMAIL_HOST_USER, settings.EMAIL_RECEIVING_USER, fail_silently = False)
            return render(request, 'school/contactussuccess.html')
    return render(request, 'school/contactus.html', {'form':sub})


from .forms import AssignTeacherToSubjectForm
from .models import Subject

def assign_teacher_to_subject(request):
    if request.method == 'POST':
        form = AssignTeacherToSubjectForm(request.POST)
        if form.is_valid():
            subject_name = form.cleaned_data['subject']
            teacher = form.cleaned_data['teacher']

            # Find or create the subject by name
            subject, created = Subject.objects.get_or_create(name=subject_name)
            subject.teacher = teacher
            subject.save()

            return redirect('admin-dashboard')  # Replace with the appropriate URL
    else:
        form = AssignTeacherToSubjectForm()
    return render(request, 'school/assign_teacher_to_subject.html', {'form': form})


from .models import TeacherExtra, Subject

@login_required
def teacher_view_subjects(request):
    teacher = TeacherExtra.objects.get(user=request.user)
    subjects = Subject.objects.filter(teacher=teacher)
    return render(request, 'school/teacher_view_subjects.html', {'subjects': subjects})


from .forms import AssignClassTeacherForm  # Import your form


def assign_class_teacher(request):
    if request.method == 'POST':
        form = AssignClassTeacherForm(request.POST)
        if form.is_valid():
            teacher = form.cleaned_data['teacher']
            assigned_class = form.cleaned_data['assigned_class']
            teacher.assigned_class = assigned_class
            teacher.save()
            return redirect('admin-dashboard')  # Redirect to admin dashboard or desired page
    else:
        form = AssignClassTeacherForm()

    return render(request, 'school/assign_class_teacher.html', {'form': form})


@login_required
def teacher_view_assigned_class(request):
    teacher = TeacherExtra.objects.get(user=request.user)
    assigned_class = teacher.assigned_class

    return render(request, 'school/teacher_view_assigned_class.html', {'teacher': teacher, 'assigned_class': assigned_class})


from .models import StudentExtra
from .forms import ClassAttendanceForm
from .models import Attendance

def take_attendance(request):
    teacher = TeacherExtra.objects.get(user=request.user)
    assigned_class = teacher.assigned_class
    students = StudentExtra.objects.filter(cl=assigned_class)

    if request.method == 'POST':
        form = ClassAttendanceForm(request.POST, students=students)
        if form.is_valid():
            attendance_date = form.cleaned_data['date']
            for student in students:
                present_status = form.cleaned_data.get(f'attendance_{student.roll}')
                # Check if an attendance record already exists for this student on this date
                existing_record = Attendance.objects.filter(roll=student.roll, date=attendance_date).first()
                if existing_record is None:
                    # If no record exists, create a new one
                    Attendance.objects.create(
                        roll=student.roll,
                        date=attendance_date,
                        cl=assigned_class,
                        present_status=present_status
                    )
            return redirect('teacher-dashboard')
    else:
        form = ClassAttendanceForm(students=students)
    return render(request, 'school/teacher_take_attendance.html', {'form': form, 'students': students})
    
from django.shortcuts import render
from .forms import AskDateForm
from .models import Attendance

def view_attendance_class(request):
    if request.method == 'POST':
        form = AskDateForm(request.POST)
        if form.is_valid():
            selected_date = form.cleaned_data['date']

            # Query attendance records for the selected date
            attendance_records = Attendance.objects.filter(date=selected_date)

            # Prepare data for the template
            data = []
            for record in attendance_records:
                data.append({
                    'roll': record.roll,
                    'date': record.date,
                    'class': record.cl,  # Replace with the actual field name for the class's name
                    'present_status': record.present_status,
                })

            return render(request, 'school/view_attendance_class.html', {'attendance': data, 'form': form})
    else:
        form = AskDateForm()
        return render(request, 'school/view_attendance_class.html', {'form': form})
    


