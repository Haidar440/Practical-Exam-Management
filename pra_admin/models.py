from django.db import models
from django.contrib.auth.models import User


# Semester Table
class Semester(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        db_table = "Ad_semester"

    def __str__(self) -> str:
        return self.name


# DIVISION TABLE
class Division(models.Model):
    name = models.CharField(max_length=5)

    class Meta:
        db_table = "Ad_division"

    def __str__(self) -> str:
        return self.name


# Subject Table
class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50)

    class Meta:
        db_table = "Ad_subject"

    def __str__(self) -> str:
        return self.name


class Lab(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        db_table = "Ad_lab"

        def __str__(self) -> str:
            return self.name


# Table of Examiner
class Examiner(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200, null=True)
    email = models.EmailField()

    class Meta:
        db_table = "Ad_examiner"

    def __str__(self) -> str:
        return self.name


# #table of Exam


class ExamSchedule(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, null=True, on_delete=models.SET_NULL)
    division = models.ForeignKey(Division, null=True, on_delete=models.SET_NULL)
    start_time = models.TimeField(
        null=True,
    )
    end_time = models.TimeField(
        null=True,
    )
    date = models.DateField(
        null=True,
    )

    class Meta:
        db_table = "Ad_ExamSchedule"

    def __str__(self) -> str:
        return self.subject.name


class Student(models.Model):
    enroll_no = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100, null=True)
    email = models.EmailField(null=True, unique=True)
    semester = models.ForeignKey(Semester, null=True, on_delete=models.SET_NULL)
    division = models.ForeignKey(Division, null=True, on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        db_table = "Ad_student"

    def __str__(self) -> str:
        return self.name


class Allocation(models.Model):
    exam = models.ForeignKey(ExamSchedule, on_delete=models.CASCADE)
    examiner = models.ForeignKey(Examiner, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    class Meta:
        db_table = "Ad_Allocation"

    def __str__(self) -> str:
        return self.exam.subject.name


class Allocation_Record(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    exam = models.ForeignKey(ExamSchedule, on_delete=models.CASCADE)
    examiner = models.ForeignKey(Examiner, on_delete=models.CASCADE)
    batch_name = models.CharField(null=True, max_length=200)
    batch_size = models.IntegerField(null=True)

    class Meta:
        db_table = "Ad_Allocation_Record"

    def __str__(self) -> str:
        return self.exam.subject.name

class Marksheet_Admin(models.Model):
    student = models.ForeignKey(Student, null=True, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester,null=True,on_delete=models.SET_NULL)
    division = models.ForeignKey(Division,null=True,on_delete=models.SET_NULL)
    pratical_marks = models.IntegerField(null=True)
    viva_marks = models.IntegerField(null=True)
    exam = models.ForeignKey(ExamSchedule, null=True, on_delete=models.CASCADE)

    class Meta:
        db_table = "Admin_Marksheet"
# Subjects allocated for the student in this exam
# Add more fields as needed (e.g., viva details, reviews)

# Additional models for exam results, viva details, reviews, etc.

# Batch Table
# class Batch(models.Model):
#      name = models.CharField(max_length=100)
#      semester = models.ForeignKey(Semester,on_delete=models.CASCADE,null=True)
#      class Meta:
#         db_table = "Ad_batch"

#      def __str__(self) -> str:
#         return self.name
