from django.urls import path
from . import views
urlpatterns = [
    path('insert/',views.inputView,name="inputdata"),
    path('viewparcels/',views.viewParcels,name="viewparcels"),
    path('viewjewellery/',views.viewJewellery,name="viewparcels"),
    path('getparcelData/',views.getParcelData,name='getparcel_data'),
    path('getjewelleryData/',views.getJewelleryData,name='getjewellery_data'),
    path('allParcels/',views.allParcels,name='allParcels'),
    path('data/', views.data_endpoint, name='data_endpoint'),
    path('update/', views.update_data_endpoint, name='update_data_endpoint'),
    path('delete/', views.delete_data_endpoint, name='delete_data_endpoint'),
    path('allJewellery/',views.allJewellery,name='allJewellery'),
    path('jewellerydata/', views. jewellerydata_endpoint, name='jewellerydata_endpoint'),
    path('jewelleryupdate/', views. jewelleryupdate_data_endpoint, name='jewelleryupdate_data_endpoint'),
    path('jewellerydelete/', views. jewellerydelete_data_endpoint, name='jewellerydelete_data_endpoint'),
]