from .models import Student
from django import forms
from django.core import validators






class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'

        widgets = {
            'first_name' : forms.TextInput(attrs={'class':'form-control'}),
            'last_name' : forms.TextInput(attrs={'class':'form-control'}),
            'school_class' : forms.TextInput(attrs={'class':'form-control'}),
            'gender' : forms.TextInput(attrs={'class':'form-control'}),
            'age' : forms.TextInput(attrs={'class':'form-control'}),
        }
