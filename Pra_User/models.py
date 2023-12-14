from django.db import models
from pra_admin.models import Student, ExamSchedule, Examiner


# Create your models here.
class Marksheet(models.Model):
    student = models.ForeignKey(Student, null=True, on_delete=models.SET_NULL)
    pratical_marks = models.IntegerField(null=True)
    viva_marks = models.IntegerField(null=True)
    exam = models.ForeignKey(ExamSchedule, null=True, on_delete=models.CASCADE)

    class Meta:
        db_table = "User_Marksheet"


# def __str__(self) -> str:
#     return self.exam.subject.name
