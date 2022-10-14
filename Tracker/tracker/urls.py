from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("signin", views.signin, name="signin"),
    path("signout", views.signout, name="signout"),
    path("create-user", views.createUser, name="create-user"),

    path("add-sample", views.addSample, name="add-sample"),
    path("add-sample/period/<int:id>", views.addSampleForPeriod, name="add-sample-period")
]