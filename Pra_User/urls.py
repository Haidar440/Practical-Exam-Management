
from django.urls import  path
from . import views
urlpatterns = [
    path("index/", views.home, name="user"),
    path('form/', views.form_submit_view, name='form_submit'),
    path("studentRecord/", views.studentRecord, name="studentRecord"),
    path("final_studentRecord/", views.final_studentRecord, name="final_studentRecord"),
]