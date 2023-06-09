from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('loadgia/',views.loadGiaData,name="giadata"),
    path('insertdiamond/',views.insertDiamond,name="insertdiamond"),
    path('stock/',views.viewStock,name="stock"),
    path('scanner/',views.scanner,name="scanner"),
    path('getmemodata/<str:scanid>',views.getMemoData,name="memo_data"),
    path('getinvoicedata/<str:scanid>',views.getinvoicedata,name='get_invoicedata'),
    path('setmemodata/',views.setMemoData,name="setmemo"),
    path('viewMemo/',views.viewMemo,name="view_memo"),
    path('preparedmemo/',views.preparedMemo,name="memo_prepared"),
    path('pdf/<str:file_name>/',views.send_pdf_response, name='pdf_response'),
    path('memodelete/<str:memo_id>',views.deleteMemo,name='memo_delete'),
    path("diamond/", views.DiamondInfo, name="diamondinfo"),
    path('setinvoicedata/',views.setInvoiceData,name="setinvoice"),
    path('gethidedata/<str:scanid>',views.getHideData,name="get_hidedata"),
    path('sethidedata/',views.setHideData,name="sethide"),
]
    
