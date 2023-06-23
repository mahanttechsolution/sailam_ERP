from django.contrib import admin
from .models import User,role
# Register your models here.
class MemberAdmin(admin.ModelAdmin):
  list_display = ("email", "role", "date_joined",)
  search_fields=["email"]

admin.site.register(User,MemberAdmin)
admin.site.register(role)