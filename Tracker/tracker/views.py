from django.contrib.auth import authenticate, login, logout
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import Job, User

def index(request):
    return HttpResponse("Hello, World!")

def signin(request):
    return render(request, "tracker/signin.html")

def createUser(request):
    
    all_jobs = list(Job.objects.all())

    return render(request, "tracker/create-user.html", {
        "jobs": all_jobs
    })