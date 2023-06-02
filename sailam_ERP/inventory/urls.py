from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('loadgia/',views.loadGiaData,name="giadata"),
    path('insertdiamond/',views.insertDiamond,name="insertdiamond"),
    path('stock/',views.viewStock,name="stock"),
    path('scanner/',views.scanner,name="scanner"),
    path('getmemodata/<str:scanid>',views.getMemoData,name="memo_data"),
    path('setmemodata/',views.setMemoData,name="setmemo"),
]