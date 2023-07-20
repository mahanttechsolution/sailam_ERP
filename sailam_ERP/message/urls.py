from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('message/',views.getMessage,name="get_message"),
    path('getlogview/',views.getLogView,name="logview"),
    path('getlogs/',views.getLog,name="getlog_data"),
]