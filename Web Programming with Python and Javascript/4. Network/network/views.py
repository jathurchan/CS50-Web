from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Post
import operator


def index(request):
    if request.method == "POST":

        # Get the username & text of the POST
        user = request.user
        text = request.POST["text"]

        # Create and save the post
        post = Post(user=user, text=text)
        post.save()
    
    
    # Get all posts and sort them : with the most recent post first
    all_posts = Post.objects.order_by('-created_at')

    return render(request, "network/index.html", {
        "posts": all_posts
    })


def error(request, errorTitle, errorMessage):
    return render(request, "network/error.html", {
        "errorTitle": errorTitle,
        "errorMessage": errorMessage
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def profile_view(request, username):

    # Attempt to get the user profile
    try:

        profile_user = User.objects.get(username=username)

        followers = profile_user.followers
        connected_username = request.user.username
        
        is_following = followers.filter(username=connected_username).count() > 0    # if 1 the connected user is already following
        connected_user = User.objects.get(username=connected_username)
        
        # Toggle Follow / Following

        if request.method == "POST":

            if is_following:
                connected_user.following.remove(profile_user)
            else:
                connected_user.following.add(profile_user)

            is_following = followers.filter(username=connected_username).count() > 0    # if 1 the connected user is already following

        # Update the counters

        following_counter = profile_user.following.count()  
        followers_counter = profile_user.followers.count()

        # Get the posts created by the profile user
        
        user_posts = Post.objects.filter(user=profile_user)
        user_posts = user_posts.order_by('-created_at')

        return render(request, "network/profile.html", {
            "username": username,
            "following_counter": following_counter,
            "followers_counter": followers_counter,
            "user_posts": user_posts,
            "is_following": is_following
        })
    except:
        return error(request, "ERROR 404", "The requested page not found !")

    
    
    
    
    
    
