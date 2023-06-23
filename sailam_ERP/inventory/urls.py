from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("loadgia/", views.loadGiaData, name="giadata"),
    path("insertdiamond/", views.insertDiamond, name="insertdiamond"),
    path("stock/", views.viewStock, name="stock"),
    path("diamond/", views.DiamondInfo, name="diamondinfo"),
    path("stock-details/", views.StockInfo, name="StockInfo"),
    path("setinvoicedata/", views.setInvoiceData, name="setinvoice"),
    path("gethidedata/<str:scanid>", views.getHideData, name="get_hidedata"),
    path("sethidedata/", views.setHideData, name="sethide"),
    path("getall/", views.getAll, name="getall_data"),
    path("allview/", views.allView, name="allview"),
    path("updateinventory/", views.updateInventory, name="updateinv"),
    path("getStk/",views.retStk,name="getStk"),
    path("getGroupView/",views.getGroupView,name="getgroupview"),
    path("getGroup/",views.getGroupData,name="getgroup"),
    path("getTally/<str:tally_id>/<str:tally_type>",views.getTallyData,name="get_tallydata"),
    path("setTally/<str:tally_type>",views.setTally,name="settally"),
    path("getTallyView/",views.getTallyView,name="gettallyview"),
    path("getTally/",views.getTally,name="gettally"),
]
