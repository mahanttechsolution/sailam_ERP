from django.urls import path
from . import views
urlpatterns = [
    path('insert/',views.inputView,name="inputdata"),
    path('viewparcels/',views.viewParcels,name="viewparcels"),
    path('viewjewellery/',views.viewJewellery,name="viewparcels"),
    path('getparcelData/',views.getParcelData,name='getparcel_data'),
    path('getjewelleryData/',views.getJewelleryData,name='getjewellery_data'),
]