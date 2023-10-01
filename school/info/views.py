from django.shortcuts import render
from django.http import HttpResponse
from .forms import StudentForm
from .models import Student
import requests
import io
import uuid
from datetime import datetime


# Create your views here.



BASE_URL = 'https://kc.kobotoolbox.org'
SUMISSION_URL = f'{BASE_URL}/api/v1/submissions'
TOKEN = '6fb29d8015dc136cba3558590282ddab7f2b24a5'


def addStudent(request):
    context = {}  # Define context outside the if-else block

    if request.method == 'POST':
        studentform = StudentForm(request.POST)
        if studentform.is_valid():
            name = studentform.cleaned_data['first_name']
            last = studentform.cleaned_data['last_name']
            school_class = studentform.cleaned_data['school_class']
            gender = studentform.cleaned_data['gender']
            age = studentform.cleaned_data['age']
            reg = Student(first_name=name, last_name=last, school_class=school_class, gender=gender, age=age)
            reg.save()

            studentform = StudentForm()
    else:
        studentform = StudentForm()

    context['form'] = studentform  # Update context with the form

    return render(request, 'addstudent.html', context)
