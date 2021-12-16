from unicodedata import name
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
    path("create", views.create, name="create"),
    path("edit", views.edit, name="edit"),
    path("modify", views.modify, name="modify"),
    path("wiki/<str:TITLE>", views.entry, name="entry")
]
