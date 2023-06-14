from django.db import models

# Create your models here.

class Parcels(models.Model):
    Id=models.BigAutoField(primary_key=True)
    Stk_Id=models.CharField(max_length=100,unique=True)
    Crt=models.FloatField()
    Clarity=models.CharField(max_length=100,null=True,blank=True)
    Desc=models.CharField(max_length=1000,null=True,blank=True)
    Price=models.FloatField()
    Color=models.CharField(max_length=100,blank=True,null=True)
    Image = models.ImageField(upload_to="media/parcels/",blank=True, null=True)
    Shape = models.CharField(max_length=100,blank=True,null=True)
    CretedBy=models.ForeignKey("account.User", on_delete=models.CASCADE,related_name='parcels_created_by')
    CreatedOn=models.DateTimeField(auto_now_add=True)
    UpdatedBy=models.ForeignKey("account.User", on_delete=models.CASCADE,related_name='parcels_updated_by',blank=True,null=True)
    UpdatedOn=models.DateTimeField(auto_now=True)
    Isdeleted=models.BooleanField(default=False)

class Jewellery(models.Model):
    Id=models.BigAutoField(primary_key=True)
    Desc=models.CharField(max_length=1000,null=True,blank=True)
    Price=models.FloatField()
    Color=models.CharField(max_length=100,blank=True,null=True)
    Image = models.ImageField(upload_to="media/jewellery/",blank=True, null=True)
    CretedBy=models.ForeignKey("account.User", on_delete=models.CASCADE,related_name='jewellery_created_by')
    CreatedOn=models.DateTimeField(auto_now_add=True)
    UpdatedBy=models.ForeignKey("account.User", on_delete=models.CASCADE,related_name='jewellery_updated_by',blank=True,null=True)
    UpdatedOn=models.DateTimeField(auto_now=True)
    Isdeleted=models.BooleanField(default=False)
    Type=models.ForeignKey("parcels_jewellery.Type",on_delete=models.CASCADE)

class Type(models.Model):
    Id=models.BigAutoField(primary_key=True)
    Name=models.CharField(max_length=100,unique=True)
    CreatedOn=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.Name
    