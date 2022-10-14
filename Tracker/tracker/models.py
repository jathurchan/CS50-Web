from email.policy import default
from turtle import title
from django.contrib.auth.models import AbstractUser
from django.db import models

class Job(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField(blank=True)

class Period(models.Model):
    startDate = models.DateField()
    endDate = models.DateField()
    isOpen = models.BooleanField(default=True)
    allotedTime = models.IntegerField()

class User(AbstractUser):
    job = models.ForeignKey("Job", blank=True, null=True, on_delete=models.CASCADE, related_name="users")
