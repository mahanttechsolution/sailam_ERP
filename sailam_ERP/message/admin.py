from django.contrib import admin
from .models import Inquiry,Message
# Register your models here.


class MessageAdmin(admin.ModelAdmin):
  list_display = ("Sender","Time")
  search_fields=["Sender"]

class InquiryAdmin(admin.ModelAdmin):
  list_display = ("id","date")
  search_fields=["date"]


admin.site.register(Message,MessageAdmin)
admin.site.register(Inquiry,InquiryAdmin)
