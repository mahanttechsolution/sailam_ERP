from django.db import models

# Create your models here.

class Message(models.Model):
    Id=models.BigAutoField(primary_key=True)
    Sender=models.ForeignKey("account.User", on_delete=models.CASCADE,related_name='message_created_by')
    Message=models.CharField(max_length=1000,null=True,blank=True)
    Time=models.DateTimeField(auto_now_add=True)
    Changes=models.TextField(null=True,blank=True)
    
class Inquiry(models.Model):
         id=models.BigAutoField(primary_key=True)
         date=models.DateTimeField(auto_now_add=True)
         inquiry=models.CharField(max_length=5000,null=True,blank=True)