import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.http.response import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from .models import User, Post
import operator


def index(request):
    
    if request.method == "POST":    # Create new post

        # Get the username & text of the POST
        user = request.user
        text = request.POST["text"]

        # Create and save the post
        post = Post(user=user, text=text)
        post.save()
    
    
    # Get all posts and sort them : with the most recent post first
    all_posts = Post.objects.order_by('-created_at')

    page_index = request.GET.get('page', 1) # Get the page index from the URL

    p = Paginator(all_posts, 10)

    try:
        c_page = p.page(page_index)
    except PageNotAnInteger:    # Get to the first page
        c_page = p.page(1)
    except EmptyPage:   # Get to the last existing page
        c_page = p.page(p.num_pages)

    c_user = None

    # Get the current signed-in user
    if request.user.is_authenticated:
        c_user = User.objects.get(username=request.user.username)

    return render(request, "network/index.html", {
        "c_page": c_page,
        "c_user": c_user
    })

@csrf_exempt
@login_required
def edit_post(request, post_id):

    # Query for requested post
    try:
        post = Post.objects.get(id=post_id)
    except:
        return JsonResponse({"error": "Post not found."}, status=404)
    
    if request.method == "POST":

        data = json.loads(request.body)

        # EDIT POST

        if request.user.username == post.user.username:

            if data.get("text") is not None:    
                post.text = data["text"]
            
            post.save()
            return JsonResponse(post.serialize())
    
    elif request.method == "PUT":
        
        data = json.loads(request.body)

        if data.get("like") is not None:
                
            c_user = User.objects.get(username=request.user.username)

            if c_user in post.likes.all():
                post.likes.remove(c_user)
            else:
                post.likes.add(c_user)
            
            return JsonResponse({
                "numberOfLikes": post.likes.count()
            })
    else:
        return JsonResponse({
                "error": "PUT request required."
            }, status=404)


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

        # Pagination

        page_index = request.GET.get('page', 1) # Get the page index from the URL

        p = Paginator(user_posts, 10)

        try:
            c_page = p.page(page_index)
        except PageNotAnInteger:    # Get to the first page
            c_page = p.page(1)
        except EmptyPage:   # Get to the last existing page
            c_page = p.page(p.num_pages)

        return render(request, "network/profile.html", {
            "username": username,
            "following_counter": following_counter,
            "followers_counter": followers_counter,
            "c_page": c_page,
            "is_following": is_following,
            "c_user": connected_user
        })
    except:
        return error(request, "ERROR 404", "The requested page not found !")


def following_view(request):

    c_user = User.objects.get(username=request.user.username)   # connected user
    
    f_users =  list(c_user.following.all()) # users followed by c_user
    
    f_posts = Post.objects.filter(user__in=f_users) # posts of f_users
    f_posts = f_posts.order_by('-created_at')

    # Pagination

    page_index = request.GET.get('page', 1) # Get the page index from the URL

    p = Paginator(f_posts, 10)

    try:
        c_page = p.page(page_index)
    except PageNotAnInteger:    # Get to the first page
        c_page = p.page(1)
    except EmptyPage:   # Get to the last existing page
        c_page = p.page(p.num_pages)

    return render(request, "network/following.html", {
        "c_page": c_page
    })