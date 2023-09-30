from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.








def addStudent(request):
    return render(request,'addstudent.html')