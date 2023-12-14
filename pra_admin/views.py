from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .decorators import unauthenticated_user, allowed_users, admin_only
from django.apps import apps
from .models import (
    Student,
    Division,
    Semester,
    Examiner,
    Subject,
    ExamSchedule,
    Allocation,
    Allocation_Record,
    Marksheet_Admin
)
from .form import (
    StudentForm,
    ExaminerForm,
    SubjectForm,
    CreateUserForm,
    ExamScheduleForm,
    AllocationForm,
    Allocation_recordForm,
)
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse
from django.core.paginator import Paginator
import pandas as pd


# Gobal Function


def upload_file(request, model_name):
    flag = 0
    # print(request.path)
    model = apps.get_model("pra_admin", model_name)

    try:
        if request.method == "POST" and request.FILES["my_file"]:
            file = request.FILES["my_file"]

            try:
                if file.name.endswith(".xlsx") or file.name.endswith(".xls"):
                    file_data = pd.read_excel(file)
                    flag = 1
                elif file.name.endswith(".csv"):
                    file_data = pd.read_csv(file)
                    flag = 1
                else:
                    raise Exception

                if flag == 1:
                    try:
                        for _, row in file_data.iterrows():
                            if model_name == "Student":
                                enroll_no = row["enroll_no"]
                                name = row["name"]
                                email = row["email"]
                                division_name = row["division"]
                                semester_name = row["semester"]
                                division = Division.objects.get(name=division_name)
                                semester = Semester.objects.get(name=semester_name)
                                print(enroll_no, name, division_name, semester)
                                model.objects.create(
                                    enroll_no=enroll_no,
                                    name=name,
                                    email=email,
                                    division=division,
                                    semester=semester,
                                )

                            #  model_name.objects.create(**dict(row))

                        return redirect("student")
                    except Exception as e:
                        messages.error(request, e)
            except Exception:
                return messages.error(request, "Unsupported file format")
    except:
        messages.error(request, "Please upload an Excel file")

    return render(request, "Admin_s/upload_file.html")


# ----------------------------------------------
# @unauthenticated_user
# def registerPage(request):
#     form = CreateUserForm()
#     if request.method == "POST":
#         form = CreateUserForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect("login")

#     context = {"form": form}
#     return render(request, "Admin_s/register.html", context)


# ----------------------------------------------
@unauthenticated_user
def loginPage(request):
    form = AuthenticationForm()
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")
    context = {"form": form}
    return render(request, "Admin_s/login.html", context)


# ----------------------------------------------
def logoutUser(request):
    logout(request)
    return redirect("login")


# ----------------------------------------------
# Create your views here.
@login_required(login_url="login")
@admin_only
def home(request):
    studentCount = Student.objects.all().count()
    context = {"studentCount": studentCount}
    return render(request, "Admin_s/index.html", context)


# ----------------------------------------------


@login_required(login_url="login")
@allowed_users(allowed_roles=["admin"])
def student(request):
    students = Student.objects.all()
    context = {
        "students": students,
    }
    return render(request, "Admin_s/student/student.html", context)

    # ----------------------------------------------

    #  def addStudent(request):
    # form = StudentForm()
    # if request.method == "POST":
    #     form = StudentForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         return redirect("student")
    # return render(request, "Admin_s/add_student.html", {"form": form})


@login_required(login_url="login")
@allowed_users(allowed_roles=["admin"])
def addStudent(request):
    form = StudentForm()
    title = "Add Student Data"
    heading = "Add Student Information"
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("student")
    context = {"form": form, "heading": heading, "title": title}
    return render(request, "Admin_s/add_form.html", context)


# ----------------------------------------------


@login_required(login_url="login")
@allowed_users(allowed_roles=["admin"])
def updateStudent(request, pri_key):
    student = Student.objects.get(id=pri_key)
    title = "Update Student Data"
    heading = "Update Student Information"
    form = StudentForm(instance=student)
    if request.method == "POST":
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect("student")
    context = {"form": form, "heading": heading, "title": title}
    return render(request, "Admin_s/add_form.html", context)


# ----------------------------------------------


@login_required(login_url="login")
@allowed_users(allowed_roles=["admin"])
def deleteStudent(request, pri_key):
    student = Student.objects.get(id=pri_key)
    student.delete()
    is_delete = Student.objects.filter(id=pri_key).exists()
    if not is_delete:
        messages.success(request, "Deleted Record SuccessFully")
    else:
        messages.error(request, "Record is not Delete")
    return redirect("student")


# ----------------------------------------------
# ----------------------------------------------

##FACULTY VIEWS


@login_required(login_url="login")
@allowed_users(allowed_roles=["admin"])
def faculty(request):
    faculty = Examiner.objects.all()
    context = {
        "facultys": faculty,
    }
    return render(request, "Admin_s/faculty/faculty.html", context)


# ----------------------------------------------


@login_required(login_url="login")
@allowed_users(allowed_roles=["admin"])
def addFaculty(request):
    title = "Add Faculty Data"
    heading = "Add Faculty Information"
    form = ExaminerForm()
    if request.method == "POST":
        form = ExaminerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("examiner")
    context = {"form": form, "heading": heading, "title": title}
    return render(request, "Admin_s/add_form.html", context)


# ----------------------------------------------


@login_required(login_url="login")
@allowed_users(allowed_roles=["admin"])
def updateExaminer(request, pri_key):
    title = "Update Faculty Data"
    heading = "Update Faculty Information"
    faculty = Examiner.objects.get(id=pri_key)
    form = ExaminerForm(instance=faculty)
    if request.method == "POST":
        form = ExaminerForm(request.POST, instance=faculty)
        if form.is_valid():
            form.save()
            return redirect("examiner")
    context = {"form": form, "heading": heading, "title": title}
    return render(request, "Admin_s/add_form.html", context)


# ----------------------------------------------


@login_required(login_url="login")
@allowed_users(allowed_roles=["admin"])
def deleteExaminer(request, pri_key):
    faculty = Examiner.objects.get(id=pri_key)
    faculty.delete()
    is_delete = Examiner.objects.filter(id=pri_key).exists()
    if not is_delete:
        messages.success(request, "Deleted Record SuccessFully")
    else:
        messages.error(request, "Record is not Delete")
    return redirect("examiner")


# ----------------------------------------------
@login_required(login_url="login")
@allowed_users(allowed_roles=["admin"])
def subject(request):
    subject = Subject.objects.all()
    context = {"subjects": subject}
    return render(request, "Admin_s/Subject/subject.html", context)


# ----------------------------------------------


@login_required(login_url="login")
@allowed_users(allowed_roles=["admin"])
def addSubject(request):
    title = "Add Subject Data"
    heading = "Add Subject Information"
    form = SubjectForm()
    if request.method == "POST":
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("subject")
    context = {"form": form, "heading": heading, "title": title}
    return render(request, "Admin_s/add_form.html", context)


# ----------------------------------------------


@login_required(login_url="login")
@allowed_users(allowed_roles=["admin"])
def updateSubject(request, pri_key):
    title = "Update Subject Data"
    heading = "Update Subject Information"
    subject = Subject.objects.get(id=pri_key)
    form = SubjectForm(instance=subject)
    if request.method == "POST":
        form = SubjectForm(request.POST, instance=subject)
        if form.is_valid():
            form.save()
            return redirect("subject")
    context = {"form": form, "heading": heading, "title": title}
    return render(request, "Admin_s/add_form.html", context)


# ----------------------------------------------


@login_required(login_url="login")
@allowed_users(allowed_roles=["admin"])
def deleteSubject(request, pri_key):
    subject = Subject.objects.get(id=pri_key)
    subject.delete()
    is_delete = Subject.objects.filter(id=pri_key).exists()
    if not is_delete:
        messages.success(request, "Deleted Record SuccessFully")
    else:
        messages.error(request, "Record is not Delete")
    return redirect("subject")


# ----------------------------------------------
@login_required(login_url="login")
@allowed_users(allowed_roles=["admin"])
def ScheduleExam(request):
    exam = ExamSchedule.objects.all()
    context = {"exams": exam}
    return render(request, "Admin_s/ScheduleExam/Exam.html", context)


# ----------------------------------------------
@login_required(login_url="login")
@allowed_users(allowed_roles=["admin"])
def addExam(request):
    title = "Add Exam Date"
    heading = "Add Exam Information"
    form = ExamScheduleForm()
    if request.method == "POST":
        form = ExamScheduleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("exam")

    context = {"form": form, "heading": heading, "title": title}
    return render(request, "Admin_s/add_form.html", context)


# ----------------------------------------------
@login_required(login_url="login")
@allowed_users(allowed_roles=["admin"])
def UpdateExam(request, pri_key):
    title = "Update Exam Date"
    heading = "Update Exam Information"
    exam = ExamSchedule.objects.get(id=pri_key)
    form = ExamScheduleForm(instance=exam)
    if request.method == "POST":
        form = ExamScheduleForm(request.POST, instance=exam)
        if form.is_valid():
            form.save()
            return redirect("exam")

    context = {"form": form, "heading": heading, "title": title}
    return render(request, "Admin_s/ScheduleExam/updateExam.html", context)


# ----------------------------------------------


@login_required(login_url="login")
@allowed_users(allowed_roles=["admin"])
def deleteExam(request, pri_key):
    exam = ExamSchedule.objects.get(id=pri_key)
    exam.delete()
    is_delete = ExamSchedule.objects.filter(id=pri_key).exists()
    if not is_delete:
        messages.success(request, "Deleted Record SuccessFully")
    else:
        messages.error(request, "Record is not Delete")
    return redirect("exam")


# ----------------------------------------------
@login_required(login_url="login")
@allowed_users(allowed_roles=["admin"])
def allocation(request):
    exam = ExamSchedule.objects.all()
    context = {"exams": exam}

    return render(request, "Admin_s/Allocation/allocation.html", context)


# ----------------------------------------------
from django.db import transaction
import json
@login_required(login_url="login")
@allowed_users(allowed_roles=["admin"])
def allocating(request, pri_key):
    title = "Allocating Student to Examiner"
    heading = "Allocating Students"
    form = AllocationForm()
    exam = ExamSchedule.objects.get(id=pri_key)
    students_data = list(Student.objects.filter(semester=exam.semester, division=exam.division).values('id', 'enroll_no'))
    students = [{'id': student['id'], 'enroll_no': student['enroll_no']} for student in students_data]
    students_json = json.dumps(students)
   
    allocated_examiners = Allocation_Record.objects.values_list('examiner__id', flat=True)
    available_examiners =list(Examiner.objects.filter(id__in=allocated_examiners).values('name'))
    examiner_name = [examiner['name'] for examiner in available_examiners]
    print(examiner_name)
    
    if request.method == "POST":
        form = AllocationForm(request.POST)
        students_id = request.POST.getlist("checks")
        if form.is_valid():
            if students_id:
                examiner_id = form.data["examiner"]
                print(examiner_id)
                examiner = Examiner.objects.get(id=examiner_id)
                print(examiner)
                print(students_id)
                for student_id in students_id:
                    student = Student.objects.get(id=student_id)
                    Allocation.objects.create(
                        exam=exam, examiner=examiner, student=student
                    )
                batch_name =  form.data['batch_name']
                batch_size = form.data['batch_size']
                allocation_record_obj = Allocation_Record.objects.create(exam=exam,examiner=examiner,batch_name=batch_name,batch_size=batch_size)
                email_send(request,allocation_record_obj)
                messages.success(request,"Successfully allocation")
                return redirect("allocation")
            else:
                messages.error(request, "Please select student")
    context = {
        "exams": exam,
        "students_json": students_json,
        "students":students_data,
        "form": form,
        "numbers": range(1, 7),
        'available_examiners': examiner_name
    }
    print(examiner_name)
    return render(request, "Admin_s/Allocation/allocation_form.html", context)

# ----------------------------------------------
@login_required(login_url="login")
@allowed_users(allowed_roles=["admin"])
def email_send(request,allocation_record):
     exam = ExamSchedule.objects.get(id=allocation_record.exam.id)
     examiner = Examiner.objects.get(id=allocation_record.examiner.id)
     subject = "Hello,Login Exam Information"
     message = "This is a from university email sent Please look"
     from_email = "haidar786sunsara@gmail.com"
     recipient_list = ["haidar786sunsara@gmail.com"]
     url = request.build_absolute_uri(reverse('login'))
     new_username,generate_password = registerPage(request,examiner.name,examiner.email,allocation_record)
     context={
            'name':allocation_record.examiner,
            'user_email':recipient_list,
            'exam_date':exam.date,
            'exam_time':exam.start_time,
            'username':new_username,
            'password':generate_password,
            'url':url,
     }
     html_message = render_to_string('Admin_s/email_template.html',context)
     send_mail(subject, message, from_email, recipient_list,html_message=html_message)
     return 


# ----------------------------------------------  
import random
import string
from django.contrib.auth.models import User
import random
import string
from django.contrib import messages
from django.contrib.auth.models import Group
@login_required(login_url="login")
@allowed_users(allowed_roles=["admin"])
def registerPage(request, username, email,allocation_record_obj):
    username = username.replace(" ", "") 
    print(username)
    if username and email: 
        if User.objects.filter(username=username).exists():
            identifier = ''.join(random.choices(string.digits, k=random.randint(3, 4)))
            identifier.strip()
            new_username = f"{username}_{identifier}"
            password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

            user = User.objects.create_user(username=new_username, password=password, email=email)
           
            return new_username,password
        else:
            user_name = username
            password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
            user = User.objects.create_user(username=user_name, password=password, email=email)
            # group = Group.objects.get(name="examiners")
            # user.groups.add(group)
            return user_name,password
    else:
        messages.error(request, "Failed to create user. Please provide a valid username and email.")

# ----------------------------------------------
@login_required(login_url="login")
@allowed_users(allowed_roles=["admin"])
def showAllocation(request,pri_key):
    exam_id = ExamSchedule.objects.get(id=pri_key)
    print(exam_id)
    allocations = Allocation.objects.filter(exam=exam_id)
    print(allocations)
    context={
        'allocations':allocations
    }
    
    return render(request,'Admin_s/Allocation/showAllocation.html',context)

# ----------------------------------------------
@login_required(login_url="login")
@allowed_users(allowed_roles=["admin"])
def updateAllocation(request,pri_key):
    allocations = Allocation.objects.get(id=pri_key)
    title = "Update Allocation Record"
    heading = "Update Allocation Information"
    form = Allocation_recordForm(instance=allocations)
    if request.method=='POST':
        form = Allocation_recordForm(request.POST,instance=allocations)
        if form.is_valid():
            form.save()
            return redirect('showAllocation',allocations.exam.id)
    print(allocations)
    context={
        'allocations':allocations,
         'form':form
    }
    
    return render(request,'Admin_s/Allocation/allocation_form.html',context)

# ----------------------------------------------
@login_required(login_url="login")
@allowed_users(allowed_roles=["admin"])
def deleteAllocation(request, pri_key):
    allocations = Allocation.objects.get(id=pri_key)
    allocation = Allocation.objects.get(id=pri_key)
    allocation.delete()
    is_delete = Allocation.objects.filter(id=pri_key).exists()
    if not is_delete:
        messages.success(request, "Deleted Record SuccessFully")
    else:
        messages.error(request, "Record is not Delete")
    return redirect('showAllocation',allocations.exam.id)

# ----------------------------------------------

@login_required(login_url="login")
@allowed_users(allowed_roles=["admin"])
def releaseData(request):
    releaseData = Allocation_Record.objects.all()
    context={
        'releaseData':releaseData
    }
    return render(request,'Admin_s/Released_Faculty/facultyData.html',context)
# ----------------------------------------------

def release(request,examiner_prikey,user_prikey):
    examiner = Examiner.objects.get(id=examiner_prikey)
    user = User.objects.get(id=user_prikey)
    examiner.delete()
    user.delete()
    is_delete_examiner = Examiner.objects.filter(id=examiner_prikey).exists()
    is_delete_user = User.objects.filter(id=user_prikey).exists()
    if not is_delete_examiner and not is_delete_user:
        messages.success(request, "Deleted Record SuccessFully")
    else:
        messages.error(request, "Record is not Delete")
    return redirect("remove")
    
def marksheet(request):
    marksheet_records = Marksheet_Admin.objects.all()
    context = {"marksheet_records": marksheet_records}
    return render(request,'Admin_s/Marksheet/marks_sheet.html',context)
# from .form import ExamDetailsForm
# def get_exam_details(request):
#     exam_details = None

#     if request.method == "POST":
#         form = ExamDetailsForm(request.POST)
#         if form.is_valid():
#             exam_details = form.get_exam_details()

#     else:
#         form = ExamDetailsForm()

#     return render(
#         request,
#         "Admin_s/Dummy/exam_details_form.html",
#         {"form": form, "exam_details": exam_details},
#     )
