from django.contrib.auth import authenticate, login, logout
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

def index(request):
    return HttpResponse("Hello, World!")
