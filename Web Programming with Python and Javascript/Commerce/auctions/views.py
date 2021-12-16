from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Bid, Comment


def index(request):

    active_listings = Listing.objects.filter(is_active=True)

    return render(request, "auctions/index.html", {
        "active_listings": active_listings
    })


def create_listing_view(request):

    if request.method == "POST":

        # Get all parameters
        title = request.POST["title"]
        description = request.POST["description"]
        starting_price = request.POST["starting_price"]
        image_url = request.POST["image_url"]
        category = request.POST["category"]

        user = User.objects.get(username=request.user.username)

        # Create a new object Listing
        listing = Listing(title=title, description=description, user=user, current_price=starting_price)
        if image_url:
            listing.image_url = image_url
        if category:
            listing.category = category
        listing.save()

        # Create the starting bid
        starting_bid = Bid(user=user, listing=listing, price=starting_price)
        starting_bid.save()

        return HttpResponseRedirect(reverse("index"))
        

    categories = [name for _, name in Listing.CATEGORY_CHOICES] # Get the names of all categories

    return render(request, "auctions/create.html", {
        "categories": categories
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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
