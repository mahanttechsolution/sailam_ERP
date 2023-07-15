from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('login/',views.login,name="login_account"),
    path('dashboard',views.dashboard,name="dashboard"),
    path('register/',views.register,name="register"),
    path('logout/',views.logoutUser),
    path('getsell/',views.fetch_data,name="get_sells"),
    path('getprofiles/',views.getUsers,name="get_profiles"),
    path('getprofileview/',views.getProfileView,name="get_profileview"),
]
