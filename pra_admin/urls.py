from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("index/", views.home, name="home"),
    path("upload_file/<str:model_name>", views.upload_file, name="upload_file"),
    path("login/", views.loginPage, name="login"),
    # path("register/", views.registerPage, name="register"),
    path("logout/", views.logoutUser, name="logout"),
    # URls of Student
    path("student/", views.student, name="student"),
    path("add_student/", views.addStudent, name="add_student"),
    path("update_student/<str:pri_key>", views.updateStudent, name="update_student"),
    path("delete_student/<str:pri_key>", views.deleteStudent, name="delete_student"),
    # URLs of Examiner
    path("examiner/", views.faculty, name="examiner"),
    path("add_examiner/", views.addFaculty, name="add_examiner"),
    path("update_examiner/<str:pri_key>", views.updateExaminer, name="update_Examiner"),
    path("delete_examiner/<str:pri_key>", views.deleteExaminer, name="delete_Examiner"),
    # URLs of subject
    path("subject/", views.subject, name="subject"),
    path("add_subject/", views.addSubject, name="add_subject"),
    path("update_subject/<str:pri_key>", views.updateSubject, name="update_subject"),
    path("delete_subject/<str:pri_key>", views.deleteSubject, name="delete_subject"),
    # URLs of Exam
    path("exam/", views.ScheduleExam, name="exam"),
    path("add_exam/", views.addExam, name="add_exam"),
    path("update_exam/<str:pri_key>", views.UpdateExam, name="update_exam"),
    path("delete_exam/<str:pri_key>", views.deleteExam, name="delete_exam"),


    # URLs of Allocation
    path("allocation/", views.allocation, name="allocation"),
    path("allocating/<str:pri_key>", views.allocating, name="allocating"),
    path("showAllocation/<str:pri_key>", views.showAllocation, name="showAllocation"),
    path("updateAllocation/<str:pri_key>", views.updateAllocation, name="updateAllocation"),
    path("deleteAllocation/<str:pri_key>", views.deleteAllocation, name="deleteAllocation"),
    
    #URLs of Remove Examiner
    path('releaseData/',views.releaseData,name='remove'),
    path('release/<str:examiner_prikey>/<str:user_prikey>',views.release,name='removed'),
    # URL pattern for getting exam details using Django form
    path('marksheet/', views.marksheet, name='marksheet'),
    # path("add_exam/", views.addExam, name="add_exam"),
    # path("update_exam/<str:pri_key>", views.UpdateExam, name="update_exam"),
    # path("delete_exam/<str:pri_key>", views.deleteExam, name="delete_exam"),
]
