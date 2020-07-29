from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
# Create your models here.
class Contact(models.Model):
    sno = models.AutoField(primary_key = True)
    name = models.CharField(max_length=30)
    phone = models.CharField(max_length=20)
    email = models.CharField(max_length=40)
    content = models.TextField()
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return 'Message from ' + self.name + ' - ' + self.email

class Userinfo(models.Model):
    username=models.CharField(max_length=30,null=True)
    firstname=models.CharField(max_length=30,null=True)
    lastname=models.CharField(max_length=30,null=True)
    email=models.CharField(max_length=30,null=True)
    password=models.CharField(max_length=30,null=True)
    phone=models.CharField(max_length=30,null=True)
    address=models.CharField(max_length=50,null=True)
    pin=models.CharField(max_length=30,null=True)
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return self.username

class DonatedFood(models.Model):
    TYPES=(('Uncooked','Uncooked'),('Cooked','Cooked'))
    no=models.AutoField(primary_key=True)
    pin=models.CharField(max_length=10,null=True)
    user=models.ForeignKey(User,null=True,on_delete=models.SET_NULL)
    foodStatus=models.CharField(max_length=200,null=True,choices=TYPES)
    phone=models.CharField(max_length=30,null=True)
    address=models.CharField(max_length=50,null=True)
    foodDescription=models.CharField(max_length=500,null=True)
    timestamp = models.DateTimeField(default=now)
    def __str__(self):
        return self.foodDescription

class DonatedCloth(models.Model):
    TYPES=(('Male','Male'),('Female','Female'))
    no=models.AutoField(primary_key=True)
    pin=models.CharField(max_length=10,null=True)
    user=models.ForeignKey(User,null=True,on_delete=models.SET_NULL)
    clothType=models.CharField(max_length=200,null=True,choices=TYPES)
    phone=models.CharField(max_length=30,null=True)
    address=models.CharField(max_length=50,null=True)
    clothDescription=models.CharField(max_length=500,null=True)
    timestamp = models.DateTimeField(default=now)
    def __str__(self):
        return self.clothDescription

class NewsFeed(models.Model):
    user1=models.CharField(max_length=30,null=True)
    feed=models.TextField(null=True)
    timestamp = models.DateTimeField(default=now)
    def __str__(self):
        return self.user1

class Notification(models.Model):
    superuser=models.CharField(max_length=30,null=True)
    enduser=models.CharField(max_length=30,null=True)
    phone=models.CharField(max_length=30,null=True)
    address=models.CharField(max_length=100,null=True)
    timestamp = models.DateTimeField(default=now)
    type1=models.CharField(max_length=100,null=True)
    description=models.CharField(max_length=500,null=True)
    done=models.IntegerField(null=True)
    def __str__(self):
        return self.enduser

class DonatedOther(models.Model):
    no=models.AutoField(primary_key=True)
    pin=models.CharField(max_length=10,null=True)
    user=models.ForeignKey(User,null=True,on_delete=models.SET_NULL)
    phone=models.CharField(max_length=30,null=True)
    address=models.CharField(max_length=50,null=True)
    otherDescription=models.CharField(max_length=500,null=True)
    timestamp = models.DateTimeField(default=now)
    def __str__(self):
        return self.otherDescription


class Finaluser(models.Model):
    superuser=models.CharField(max_length=30,null=True)
    enduser=models.CharField(max_length=30,null=True)
    phone=models.CharField(max_length=30,null=True)
    address=models.CharField(max_length=100,null=True)
    timestamp = models.DateTimeField(default=now)
    type1=models.CharField(max_length=100,null=True)
    description=models.CharField(max_length=500,null=True)
    done=models.IntegerField(null=True)
    def __str__(self):
        return self.enduser
