from django.db import models

# Create your models here.


class Student(models.Model):
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_lenth=100)
    last_name = models.CharField(max_length=100)

