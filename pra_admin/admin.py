from django.contrib import admin
from .resources import StudentResource
from import_export.admin import ImportExportModelAdmin
from .models import (
    Student,
    Division,
    Semester,
    Subject,
    ExamSchedule,
    Examiner,
    Allocation,
    Allocation_Record,
    Marksheet_Admin,
)


# Register your models here.
@admin.register(Student)
class StudentAdmin(ImportExportModelAdmin):
    list_display = ("enroll_no", "name", "email", "semester", "division")


class SemesterAdmin(admin.ModelAdmin):
    list_display = ("name",)


admin.site.register(Semester, SemesterAdmin)


class DivisionAdmin(admin.ModelAdmin):
    list_display = ("name",)


admin.site.register(Division, DivisionAdmin)


class SubjectAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "code",
    )


admin.site.register(Subject, SubjectAdmin)


class ExaminerAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "address",
        "email",
    )


admin.site.register(Examiner, ExaminerAdmin)


class ExamScheduleAdmin(admin.ModelAdmin):
    list_display = (
        "subject",
        "semester",
        "division",
        "start_time",
        "end_time",
        "date",
    )


admin.site.register(ExamSchedule, ExamScheduleAdmin)


class AllocationAdmin(admin.ModelAdmin):
    list_display = (
        "exam",
        "examiner",
        "student",
    )


admin.site.register(Allocation, AllocationAdmin)


class Allocation_RecordAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "exam",
        "examiner",
        "batch_name",
        "batch_size",
    )


admin.site.register(Allocation_Record, Allocation_RecordAdmin)


class Marksheet_Admin1(admin.ModelAdmin):
    list_display = (
        "student",
        "exam",
        "semester",
        "division",
        "pratical_marks",
        "viva_marks",
    )


admin.site.register(Marksheet_Admin, Marksheet_Admin1)
