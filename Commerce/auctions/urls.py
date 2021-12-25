from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("l/<str:listing_id>", views.listing_view, name="listing"),
    path("watchlist", views.watchlist_view, name="watchlist"),
    path("categories", views.categories_view, name="categories"),
    path("create", views.create_listing_view, name="create"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]
