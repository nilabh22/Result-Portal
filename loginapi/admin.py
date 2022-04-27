from django.contrib import admin
from import_export.admin import ImportExportActionModelAdmin
from .models import Student
# Register your models here.


@admin.register(Student)
class StudentAdmin(ImportExportActionModelAdmin):
    pass