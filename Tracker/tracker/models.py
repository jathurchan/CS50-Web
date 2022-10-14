from turtle import title
from django.contrib.auth.models import AbstractUser
from django.db import models

class Job(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField(blank=True)


class User(AbstractUser):
    job = models.ForeignKey("Job", on_delete=models.CASCADE, related_name="users")
