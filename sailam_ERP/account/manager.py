from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    use_in_migrations=True

    def create_user(self,email,firstname,lastname,password,**extra_fields):
        email=self.normalize_email(email)
        user=self.model(email=email,last_name=lastname,first_name=firstname,**extra_fields)
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_active',True)
        user.set_password(password)
        user.save(using=self._db)
        return user
    

    def create_staffuser(self, email, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password,first_name,last_name):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            firstname=first_name,
            lastname =last_name,
            password=password,
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user