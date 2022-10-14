from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import Job, User, Period


def index(request):
    return HttpResponse("Hello, World!")


def signin(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        print(username)
        print(password)
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("add-sample"))
        else:
            return render(request, "tracker/signin.html", {
                "message": "Invalid username or password."
            })
    else:
        return render(request, "tracker/signin.html")


def signout(request):
    logout(request)
    return HttpResponseRedirect(reverse("signin"))


def createUser(request):
    if request.method == "POST":
        username = request.POST["username"]

        firstName = request.POST["firstName"]
        lastName = request.POST["lastName"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "tracker/create-user.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username=username, first_name=firstName, last_name=lastName, password=password)
            user.job = Job.objects.get(id=request.POST["job_id"])
            print(user.job)
            user.save()
        except IntegrityError:
            return render(request, "tracker/create-user.html", {
                "message": "Username already taken."
            })
        return HttpResponseRedirect(reverse("index"))
    
    all_jobs = list(Job.objects.all())

    return render(request, "tracker/create-user.html", {
        "jobs": all_jobs
    })

@login_required
def addSample(request):
    if request.method == "POST" :
        try:
            return addSampleForPeriod(request, request.POST["period_id"])
        except:
            pass
        
    open_periods = list(Period.objects.filter(isOpen=True))
    return render(request, "tracker/add-sample.html", {
        "open_periods": open_periods
    })

@login_required
def addSampleForPeriod(request, id):

    period = Period.objects.get(id=id)

    return render(request, "tracker/add-sample.html", {
        "selected_period": period
    })