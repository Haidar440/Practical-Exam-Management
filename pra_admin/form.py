from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import (
    Student,
    Examiner,
    Subject,
    ExamSchedule,
    Allocation,
    Allocation_Record,
)


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = "__all__"


class ExaminerForm(forms.ModelForm):
    class Meta:
        model = Examiner
        fields = "__all__"


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = "__all__"


class ExamScheduleForm(forms.ModelForm):
    class Meta:
        model = ExamSchedule
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["date"].widget = forms.DateInput(format="%d/%m/%Y")
        self.fields["date"].input_formats = ["%d/%m/%Y", "%Y-%m-%d"]
        self.fields["start_time"].widget = forms.TimeInput(attrs={"type": "time"})
        self.fields["end_time"].widget = forms.TimeInput(attrs={"type": "time"})
        self.fields["date"].widget = forms.DateInput(attrs={"type": "date"})


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class AllocationForm(forms.ModelForm):
    class Meta:
        model = Allocation
        fields = "__all__"
        exclude = ['student','exam'] 
    batch_name = forms.CharField(max_length=100)
    batch_size = forms.IntegerField(min_value=1)

class Allocation_recordForm(forms.ModelForm):
    class Meta:
        model = Allocation
        fields = "__all__"

    # def save(self, commit=True):

    #     allocation = super().save(commit=commit)
    #     batch_size = self.data['batch_size']
    #     batch_name = self.data['batch_name']
    #     Allocation_Record.objects.create(exam=allocation.exam,examiner=allocation.examiner,batch_name=batch_name,batch_size=batch_size)
    #     return allocation
        # exclude = ['student']


# forms.py
from django import forms
from .models import ExamSchedule


# class ExamDetailsForm(forms.Form):
#     exam = forms.ModelChoiceField(
#         queryset=ExamSchedule.objects.all(), empty_label="Select Exam"
#     )

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields["exam"].widget.attrs[
#             "class"
#         ] = "form-control"  # Add Bootstrap class

#     def get_exam_details(self):
#         exam_id = self.cleaned_data.get("exam")
#         if exam_id:
#             exam = ExamSchedule.objects.get(id=exam_id)
#             print(exam)
#             return exam
#         return None
