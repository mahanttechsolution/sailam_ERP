from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("", views.login, name="login"),
    path("register/", views.register),
    path("logout/", views.auth_logout, name="logout"),
]
