from django.contrib import admin
from .models import Student

# Register your models here.


@admin.register(Student)

class StudentAdmin(admin.ModelAdmin):
    list_display = ['first_name','last_name','school_class','gender','age']
