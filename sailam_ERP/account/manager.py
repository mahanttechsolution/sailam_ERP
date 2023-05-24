from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    use_in_migrations=True

    def _create_user(self,email,firstname,lastname,password,**extra_fields):
        email=self.normalize_email(email)
        user=self.model(email=email,last_name=lastname,first_name=firstname,**extra_fields)
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_active',True)
        user.set_password(password)
        user.save(using=self._db)
        return user