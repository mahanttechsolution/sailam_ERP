from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("stocks/", views.stocks, name="stocks"),
    path("filter/", views.filter_data, name="filter"),
]