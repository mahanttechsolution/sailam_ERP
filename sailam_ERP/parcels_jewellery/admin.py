from django.contrib import admin
from .models import Color, Parcels,Type,Jewellery
# Register your models here.
class MemberParcel(admin.ModelAdmin):
  list_display = ("Stk_Id", "Crt", "Color","CretedBy")
  search_fields=["Stk_Id","Color"]

class MemberJewellery(admin.ModelAdmin):
  list_display = ("Id","Type" ,"Price", "Color","CretedBy")
  search_fields=["Id","Type__Name"]
  def Type(self, obj):
        return obj.Type.Name
  
admin.site.register(Parcels,MemberParcel)
admin.site.register(Jewellery,MemberJewellery)
admin.site.register(Type)
admin.site.register(Color)