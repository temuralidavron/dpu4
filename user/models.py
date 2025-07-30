from datetime import timedelta

from django.contrib.auth.models import AbstractUser
from django.db import models
import random

from django.utils import timezone


class Role(models.TextChoices):
    ADMIN=('admin','Admin')
    WRITER=('writer','Writer')
    READER=('reader','Reader')

class CustomUser(AbstractUser):
    phone = models.CharField(max_length=20, null=True, blank=True)
    role=models.CharField(max_length=20,choices=Role,default=Role.READER)
    email=models.EmailField(max_length=100)

def get_code():
    return random.randint(100000,999999)

def checking_time():
    return timezone.now()+timedelta(minutes=2)

class Code(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    code=models.CharField(max_length=6,default=get_code)
    expire_date=models.DateTimeField(default=checking_time)



class Profile(models.Model):
    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE,related_name='profile')
    nickname=models.CharField(max_length=20,blank=True,null=True)
    bio=models.TextField(blank=True,null=True)
    image=models.ImageField(default='person.png',upload_to='profile',blank=True,null=True)

