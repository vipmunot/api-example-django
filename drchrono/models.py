from django.db import models

from datetime import datetime

# Create your models here.


class Patient(models.Model):
    first_name = models.CharField(default="",max_length=20);
    last_name = models.CharField(default="",max_length=20);
    doctor = models.PositiveIntegerField(default=-1);
    gender = models.CharField(default="Male",max_length=60);
    date_of_birth = models.CharField(default=str(datetime.now()), max_length= 10);


# python manage.py makemigrations
# python manage.py migrate

class User(models.Model):
    user_name = models.CharField(max_length=20);
    access_token = models.CharField(max_length=100);
