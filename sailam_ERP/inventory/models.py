from django.db import models

# Create your models here.
class inventory(models.Model):
    Id=models.BigAutoField(primary_key=True)
    STK_ID=models.CharField(max_length=100,unique=True)
    SHAPE=models.CharField(max_length=100,blank=True,null=True)
    COLOR=models.CharField(max_length=100,blank=True,null=True)
    CLARITY=models.CharField(max_length=100,blank=True,null=True)
    POL=models.CharField(max_length=100,blank=True,null=True)
    SYM=models.CharField(max_length=100,blank=True,null=True)
    CUT=models.CharField(max_length=100,blank=True,null=True)
    FLO_COL=models.CharField(max_length=100,blank=True,null=True)
    MESUREMNT=models.CharField(max_length=100,blank=True,null=True)
    DEPTH=models.FloatField(blank=True,null=True)
    TABLE=models.FloatField(blank=True,null=True)
    GIA_NO=models.CharField(max_length=100,blank=True,null=True)
    REMARK=models.CharField(max_length=500,blank=True,null=True)
    PRICE=models.FloatField()
    CRT=models.FloatField()
    DESCRIPTION=models.TextField(blank=True,null=True)
    CretedBy=models.ForeignKey("account.User", on_delete=models.CASCADE,related_name='inventory_created_by')
    CreatedOn=models.DateTimeField(auto_now_add=True)
    UpdatedBy=models.ForeignKey("account.User", on_delete=models.CASCADE,related_name='inventory_updated_by',blank=True,null=True)
    UpdatedOn=models.DateTimeField(auto_now=True)
    Scan_Id=models.BigIntegerField(blank=True,null=True)
    MemoMade=models.BooleanField(default=False)

class ActivityLog(models.Model):
    Log_Id=models.AutoField(primary_key=True)
    User=models.ForeignKey("account.User", on_delete=models.CASCADE)
    TimeStamp=models.DateTimeField(auto_now_add=True)
    Log_message=models.TextField()
    Notified=models.BooleanField(default=False)

class Video(models.Model):
    id_inv=models.ForeignKey("inventory.inventory",on_delete=models.CASCADE)
    file = models.FileField(upload_to='uploads/videos/',blank=True,null=True)
    image = models.ImageField(upload_to='uploads/images/',blank=True,null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
class Memo(models.Model):
    id_memo=models.BigAutoField(primary_key=True)
    client=models.ForeignKey("inventory.client",on_delete=models.CASCADE)
    is_deleted=models.BooleanField(default=False)
    CretedBy=models.ForeignKey("account.User", on_delete=models.CASCADE,related_name='memo_created_by')
    CreatedOn=models.DateTimeField(auto_now_add=True)

class MemoData(models.Model):
    memo=models.ForeignKey("inventory.Memo",on_delete=models.CASCADE)
    stk_no=models.ForeignKey("inventory.inventory", to_field='STK_ID', on_delete=models.CASCADE)
    desc=models.CharField(max_length=500,blank=True,null=True)
    weight=models.FloatField()
    rate=models.FloatField()
    remark=models.CharField(max_length=500,blank=True,null=True)
    
class Client(models.Model):
    id_client=models.BigAutoField(primary_key=True)
    name=models.CharField(max_length=500,blank=True,null=True)
    company=models.CharField(max_length=500,blank=True,null=True)
    address=models.TextField()

    def __str__(self):
        return "Name: "+self.name+" Company: "+self.company+" Address: "+self.address
    