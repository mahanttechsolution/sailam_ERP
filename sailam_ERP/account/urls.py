from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('',views.login,name="login_account"),
    path('register/',views.register),
    path('logout/',views.logoutUser),
]