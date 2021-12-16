from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.deletion import CASCADE, RESTRICT


class User(AbstractUser):
    pass


class Listing(models.Model):
    
    CATEGORY_CHOICES = [
        ('MO', 'Motors'),
        ('FA', 'Fashion'),
        ('EL', 'Electronics'),
        ('CA', 'Collectibles & Art'),
        ('HG', 'Home & Garden'),
        ('SG', 'Sporting Goods'),
        ('TO', 'Toys'),
        ('MU', 'Music'),
        ('ER', 'eBay Refurbished')
    ]

    title = models.CharField(max_length=64)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_listings")

    current_price = models.DecimalField(default=0, max_digits=8, decimal_places=2)

    image_url = models.URLField(blank=True)
    category = models.CharField(max_length=2, blank=True, choices=CATEGORY_CHOICES)

    is_active = models.BooleanField(default=True)
    winner = models.ForeignKey(User, blank=True, null=True, on_delete=RESTRICT, related_name="winner_listings")

    watchers = models.ManyToManyField(User, blank=True, related_name="watchlist")


class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE, related_name="user_bids")
    listing = models.ForeignKey(Listing, on_delete=CASCADE, related_name="listing_bids")
    price = models.DecimalField(max_digits=8, decimal_places=2)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE, related_name="user_comments")
    listing = models.ForeignKey(Listing, on_delete=CASCADE, related_name="listing_comments")
    text = models.TextField()