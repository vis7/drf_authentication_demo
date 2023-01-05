from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import UserManager

class MyAccountManager(BaseUserManager):
    def create_user(
            self, email, fullname=None, birthday=None, zipcode=None,password=None
        ):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            Email_Address=self.normalize_email(email),
            name=self.normalize_email(email),
            Date_of_Birth=birthday,
            zipcode=zipcode,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, Email_Address, password):
        user = self.create_user(
            Email_Address=self.normalize_email(Email_Address),
            password=password,
        )
        user.is_admin = True
        user.is_active=True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

# Create your models here.
class User(AbstractBaseUser):
    objects = UserManager()
    USERNAME_FIELD = 'username'

    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return "User: " + self.username
    

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

class Customer(User):
    GENDER = (
        ('male', 'Male'),
        ('female', 'Female')
    )

    phone_number = PhoneNumberField(null=True, blank=True, unique=True)
    profile_photo = models.ImageField(upload_to='profile_pics/', default='user_default_profile.jpg')
    gender = models.CharField(max_length=10, choices=GENDER, default='male', null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)

    def __str__(self):
        return "Customer: " + self.username

    
