from typing import List
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Listing, Bid, Comment


def index(request):

    active_listings = Listing.objects.filter(is_active=True)

    return render(request, "auctions/index.html", {
        "active_listings": active_listings
    })


@login_required
def categories_view(request):

    categories = [name for _, name in Listing.CATEGORY_CHOICES] # Get the names of all categories
    c_listings = Listing.objects.filter(is_active=True)  # Get all listings
    c_category = None

    if request.method == "GET":
        if request.GET.get('c'):
            c_category = request.GET['c'].capitalize()
            
            if c_category in categories:
                c_listings = Listing.objects.filter(category=c_category, is_active=True)
            else:
                c_category = None

    return render(request, "auctions/categories.html", {
        "categories": categories,
        "c_category": c_category,
        "c_listings": c_listings
    })


@login_required
def watchlist_view(request):
    try:
        user = User.objects.get(username=request.user)

        watchlist = user.watchlist.all()
        print(watchlist)

        return render(request, "auctions/watchlist.html", {
            "watchlist": watchlist
        })
    except:
        return render(request, "auctions/error.html", {
            "message": "Error 404 Page Not Found"
        })


@login_required
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
        listing.temp_winner = user
        listing.save()

        # Create the starting bid
        starting_bid = Bid(user=user, listing=listing, price=starting_price)
        starting_bid.is_starting_bid = True
        starting_bid.save()

        return HttpResponseRedirect(reverse("index"))
        

    categories = [name for _, name in Listing.CATEGORY_CHOICES] # Get the names of all categories

    return render(request, "auctions/create.html", {
        "categories": categories
    })


def listing_view(request, listing_id):
    
    # Get the listing
    try:
        listing = Listing.objects.get(id=listing_id)
    except:
        return render(request, "auctions/error.html", {
            "message": "Error 404: Listing not found."
        })

    is_c_user_watching, is_c_user_winner = False, False

    # Get the current signed in user (if signed in)

    c_user = User.objects.get(username=request.user.username)

    is_c_user_watching = c_user in listing.watchers.all()
    is_c_user_creator = c_user == listing.user

    bid_error = False

    # If signed in, ability to add a bid & add / remove from watchlist & Close the listing
    if request.method == "POST":

        if 'bid_form' in request.POST:  # add a bid
            bid_price = int(request.POST["bid"])
            # starting bid? => equal or lower ELSE strictly lower
            if ((listing.listing_bids.count() == 1) and (listing.current_price <= bid_price)) or (listing.current_price < bid_price):
                bid = Bid(user=c_user, listing=listing, price=bid_price)
                bid.save()
                listing.current_price = bid_price
                listing.temp_winner = c_user
                listing.save()
            else:
                bid_error = True
                
        elif 'watchlist_form' in request.POST:  # add / remove c_user from watchlist
            if is_c_user_watching:
                listing.watchers.remove(c_user)
            else:
                listing.watchers.add(c_user)
            is_c_user_watching = c_user in listing.watchers.all()   # update
        
        elif 'close_form' in request.POST:
            listing.is_active = False
            listing.save()
        
        elif 'comment_form' in request.POST:
            comment_text = request.POST["text"]
            comment = Comment(user=c_user, listing=listing, text=comment_text)
            comment.save()
        
    is_c_user_winner = c_user == listing.temp_winner    # update current winner

    listing_comments = listing.listing_comments.all()

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "is_c_user_watching": is_c_user_watching,
        "is_c_user_winner": is_c_user_winner,
        "is_c_user_creator": is_c_user_creator,
        "bid_error": bid_error,
        "listing_comments": listing_comments
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
