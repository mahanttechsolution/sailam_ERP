from django.contrib import admin
from .models import Parcels,Type
# Register your models here.
class MemberParcel(admin.ModelAdmin):
  list_display = ("Stk_Id", "Crt", "Color","CretedBy")

admin.site.register(Parcels,MemberParcel)
admin.site.register(Type)