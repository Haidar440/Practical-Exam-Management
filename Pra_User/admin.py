from django.contrib import admin
from .models import Marksheet
# Register your models here.
class Marsheetadmin(admin.ModelAdmin):
    list_display=('student','pratical_marks','viva_marks','exam')
admin.site.register(Marksheet,Marsheetadmin)
