from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    
    path("stocks/", views.stocks, name="stocks"),
    path("filter/", views.filter_data, name="filter"),
    path("jewelry/", views.jewelry, name="jewelry"),
    path("parcel/", views.parcel, name="parcel"),
    path("download/", views.download, name="download"),
]