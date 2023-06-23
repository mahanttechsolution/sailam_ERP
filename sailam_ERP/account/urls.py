from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('',views.login,name="login_account"),
    path('register/',views.register),
    path('logout/',views.logoutUser),
    path('getsell/',views.fetch_data,name="get_sells"),
    path('getprofiles/',views.getUsers,name="get_profiles"),
    path('getprofileview/',views.getProfileView,name="get_profileview"),
]