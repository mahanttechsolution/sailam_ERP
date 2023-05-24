from django.contrib import admin
from .models import User
# Register your models here.
class MemberAdmin(admin.ModelAdmin):
  list_display = ("email", "role", "date_joined",)

admin.site.register(User,MemberAdmin)