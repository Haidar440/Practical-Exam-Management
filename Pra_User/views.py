from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from pra_admin.models import Allocation, Allocation_Record, Student, ExamSchedule,Marksheet_Admin,Semester,Division,Subject
from .models import Marksheet
from django.contrib import messages
from django.contrib.auth.models import User
from .decorators import unauthenticated_user, allowed_users, admin_only
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required(login_url="login")
def home(request):
    allocation_record = Allocation.objects.all().filter(
        examiner=request.user.allocation_record.examiner
    )
    totalStudentAllocation = allocation_record.count()

    context = {"totalStudent": totalStudentAllocation}

    return render(request, "User_s/index.html", context)


@login_required(login_url="login")
def studentRecord(request):
    allocation = Allocation_Record.objects.filter(user=request.user)
    for record in allocation:
        exam_id = record.exam.id

    if request.method == "POST":
        for key in request.POST:
            if key.startswith("row-"):
                marksheet_id = key.split("-")[1]
                practical_marks = request.POST.get(f"row-{marksheet_id}", None)
                viva_marks = request.POST.get(f"row-{marksheet_id}-viva", None)

                if practical_marks and viva_marks and exam_id:
                    print(practical_marks)
                    try:
                        # Convert practical_marks and viva_marks to integers
                        practical_marks = int(practical_marks)
                        viva_marks = int(viva_marks)

                        if practical_marks is None or practical_marks >= 1:
                            if viva_marks is None or viva_marks >= 1:
                                student_id = int(
                                    marksheet_id
                                )  # Assuming marksheet_id is the student ID in this case
                                student = Student.objects.get(id=student_id)
                                exam = ExamSchedule.objects.get(id=exam_id)

                                # Check if Marksheet instance already exists for this student and exam
                                marksheet, created = Marksheet.objects.get_or_create(
                                    student=student, exam=exam
                                )
                                # Update the practical and viva marks
                                marksheet.pratical_marks = int(practical_marks)
                                marksheet.viva_marks = int(viva_marks)
                                marksheet.save()
                            else:
                                messages.error(
                                    request,
                                    "viva_marks should be greater than or equal to 1 or None",
                                )
                        else:
                            messages.error(
                                request,
                                "practical_marks should be greater than or equal to 1 or None",
                            )
                    except ValueError as e:
                        messages.error(request, f"Error: {e}")
        return HttpResponseRedirect(request.path_info)
   
       
def final_studentRecord(request):
    allocation = Allocation_Record.objects.filter(user=request.user)
    for record in allocation:
        exam_id = record.exam.id

    if request.method == "POST":
        for key in request.POST:
            # print(key)
            if key.startswith("row-"):
                # print(request.POST)
                marksheet_id = key.split("-")[1]
                practical_marks = request.POST.get(f"row-{marksheet_id}")
                
                viva_marks = request.POST.get(f"row-{marksheet_id}-viva", None)
                if practical_marks.strip() != '' and viva_marks.strip() != '':
                    if practical_marks and viva_marks and exam_id:
                        try:
                            # Convert practical_marks and viva_marks to integers
                            practical_marks = int(practical_marks)
                            viva_marks = int(viva_marks)

                            if practical_marks is None or practical_marks >= 1:
                                if viva_marks is None or viva_marks >= 1:
                                    student_id = int(
                                        marksheet_id
                                    )  # Assuming marksheet_id is the student ID in this case
                                    student = Student.objects.get(id=student_id)
                                    exam = ExamSchedule.objects.get(id=exam_id)

                                    # Check if Marksheet instance already exists for this student and exam
                                    marksheet, created = Marksheet.objects.get_or_create(
                                        student=student, exam=exam
                                    )
                                    # Update the practical and viva marks
                                    marksheet.pratical_marks = int(practical_marks)
                                    marksheet.viva_marks = int(viva_marks)
                                    marksheet.save()
                                    
                                    # print(exam.semester.id) 
                                    semester = Semester.objects.get(id=exam.semester.id)
                                    division = Division.objects.get(id=exam.division.id)
                                    
                                    
                                    marksheet_admin, created = Marksheet_Admin.objects.get_or_create(
                                        student=student, exam=exam,semester=semester,division=division
                                    )
                                    # Update the practical and viva marks
                                    marksheet_admin.pratical_marks = int(practical_marks)
                                    marksheet_admin.viva_marks = int(viva_marks)
                                    marksheet_admin.save()

                        
                                else:
                                    messages.error(
                                        request,
                                        "viva_marks should be greater than or equal to 1 or None",
                                    )
                            else:
                                messages.error(
                                    request,
                                    "practical_marks should be greater than or equal to 1 or None",
                                )
                        except ValueError as e:
                            messages.error(request, f"Error: {e}")
                else: 
                    messages.error(request, "Both practical and viva marks must be filled")
                    break

        return HttpResponseRedirect(request.path_info)
   
       


   
    


def form_submit_view(request):
    if request.method == 'POST':
        submit_action = request.POST.get('submit_action')
        print(submit_action)
        if submit_action == 'studentRecord':
            return studentRecord(request)
        elif submit_action == 'final_studentRecord':
            return final_studentRecord(request)
    #  if Allocation_Record.objects.exists():
    allocation_record = Allocation.objects.all().filter(
        examiner=request.user.allocation_record.examiner
    )
    marksheet_records = []
    for record in allocation_record:
        # Fetch the Marksheet instance if it exists for the current student
        marksheet = Marksheet.objects.filter(student=record.student).first()
        marksheet_records.append((record, marksheet))

    context = {"marksheet_records": marksheet_records}
    return render(request, "User_s/studentRecord.html",context)


    
