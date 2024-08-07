from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("loadgia/", views.loadGiaData, name="giadata"),
    path("insertdiamond/", views.insertDiamond, name="insertdiamond"),
    path("stock/", views.viewStock, name="stock"),
    path("scanner/", views.scanner, name="scanner"),
    path("getmemodata/<str:scanid>", views.getMemoData, name="memo_data"),
    path("getinvoicedata/<str:scanid>", views.getinvoicedata, name="get_invoicedata"),
    path("setmemodata/", views.setMemoData, name="setmemo"),
    path("viewMemo/", views.viewMemo, name="view_memo"),
    path("viewHidden/", views.viewHidden, name="hiddenstock"),
    path("preparedmemo/", views.preparedMemo, name="memo_prepared"),
    path("hidestock/", views.getHideStock, name="hide_stock"),
    path("show/<str:stk_id>", views.showDiamond, name="show_diamond"),
    path("pdf/<str:file_name>/", views.send_pdf_response, name="pdf_response"),
    path("memodelete/<str:memo_id>", views.deleteMemo, name="memo_delete"),
    path("diamond/", views.DiamondInfo, name="diamondinfo"),
    path("stock-details/", views.StockInfo, name="StockInfo"),
    # path("filter/", views.filter, name="filter"),
    path("setinvoicedata/", views.setInvoiceData, name="setinvoice"),
    path("gethidedata/<str:scanid>", views.getHideData, name="get_hidedata"),
    path("sethidedata/", views.setHideData, name="sethide"),
    path("getall/", views.getAll, name="getall_data"),
    path("allview/", views.allView, name="allview"),
    path("updateinventory/", views.updateInventory, name="updateinv"),
    path("deleteInventory/", views.deleteInventory, name="deleteinv"),
    path("getStk/",views.retStk,name="getStk"),
    path("getGroupView/",views.getGroupView,name="getgroupview"),
    path("getGroup/",views.getGroupData,name="getgroup"),
    path("getTally/<str:tally_id>/<str:tally_type>",views.getTallyData,name="get_tallydata"),
    path("setTally/<str:tally_type>",views.setTally,name="settally"),
    path("getTallyView/",views.getTallyView,name="gettallyview"),
    path("getTally/",views.getTally,name="gettally"),
]
