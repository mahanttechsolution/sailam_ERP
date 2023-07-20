from django.contrib import admin

from inventory.models import Location,Client,inventory,Invoice,InvoiceData,Memo,MemoData,Tally,TallyData,Video

class InventoryAdmin(admin.ModelAdmin):
  list_display = ("STK_ID","CRT","CreatedOn")
  search_fields=["STK_ID"]

class ClientAdmin(admin.ModelAdmin):
  list_display = ("name","company","address")
  search_fields=["name","company"]

class InvoiceAdmin(admin.ModelAdmin):
  list_display = ("client","CretedBy","CreatedOn")
  search_fields=["client__name","CretedBy__email"]

class InvoiceDataAdmin(admin.ModelAdmin):
  list_display = ('STK_ID',"desc","weight","cfr","total")
  search_fields=["stk_no__STK_ID","weight"]
  def STK_ID(self, obj):
        return obj.stk_no.STK_ID

class MemoAdmin(admin.ModelAdmin):
    list_display = ("client","CretedBy","CreatedOn")
    search_fields=["client__name","CretedBy__email"]

class MemoDataAdmin(admin.ModelAdmin):
  list_display = ('STK_ID',"desc","weight","rate")
  search_fields=["stk_no__STK_ID","weight"]
  def STK_ID(self, obj):
        return obj.stk_no.STK_ID

class TallyAdmin(admin.ModelAdmin):
  list_display = ("Name","CretedBy","CreatedOn")
  search_fields=["Name","CretedBy__email"]

class TallyDataAdmin(admin.ModelAdmin):
  list_display = ("stk_no","Name","submitted")
  search_fields=["stk_no__STK_ID"]
  def Name(self, obj):
     return obj.tally_no.Name
class VideoAdmin(admin.ModelAdmin):
  list_display = ("STK_ID","uploaded_at")
  search_fields=["id_inv__STK_ID"]
  def STK_ID(self, obj):
        return obj.id_inv.STK_ID
# Register your models here.
admin.site.register(Location)
admin.site.register(inventory,InventoryAdmin)
admin.site.register(Client,ClientAdmin)
admin.site.register(Invoice,InvoiceAdmin)
admin.site.register(InvoiceData,InvoiceDataAdmin)
admin.site.register(Memo,MemoAdmin)
admin.site.register(MemoData,MemoDataAdmin)
admin.site.register(Tally,TallyAdmin)
admin.site.register(TallyData,TallyDataAdmin)
admin.site.register(Video,VideoAdmin)