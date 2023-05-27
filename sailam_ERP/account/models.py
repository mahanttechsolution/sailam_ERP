from django.db import models
from django.contrib.auth.models import AbstractUser,PermissionsMixin
from .manager import UserManager

choice = (
    (1, ("admin")),
    (2, ("manager")),
    (3, ("salesmen")),
    (4, ("user")),
)
status={
    (1, ("active")),
    (2, ("passive")),
}
class role(models.Model):
    role_id=models.IntegerField(primary_key=True)
    role_name=models.CharField(choices=choice,default=4,max_length=20)
    role_status=models.CharField(choices=status,default=1,max_length=20)
    
    def __str__(self):
         return self.role_name
    

class User(AbstractUser,PermissionsMixin):
   role=models.ForeignKey(
        role,
        on_delete=models.CASCADE,
        default=4
    )
   username=None
   email=models.EmailField(('email address'),unique=True)
   USERNAME_FIELD='email'
   REQUIRED_FIELDS=['first_name','last_name']
   objects=UserManager()

