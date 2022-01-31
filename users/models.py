from django.db import models
from django.utils import timezone
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)

# Create your models here.
# UserManager class code here
class MyUserManager(BaseUserManager):
  def create_user(self, email,password=None):
    """
    Creates and saves a User with the given email,and password.
    """
    if not email:
        raise ValueError('Users must have an email address')

    user = self.model(email=self.normalize_email(email))
    user.set_password(password)
    user.save(using=self._db)
    return user
 
  def create_superuser(self, email,password=None):
    """
    Creates and saves a superuser with the given email, date of
    birth and password.
    """
    user = self.create_user(email,password=password)
    user.is_admin = True
    user.save(using=self._db)
    return user

# Custom User Model
class User(AbstractBaseUser):
  email       = models.EmailField(verbose_name='email address',unique=True)
  first_name  = models.CharField(max_length=200,verbose_name='First Name',blank=True)
  last_name   = models.CharField(max_length=200,verbose_name='Last Name',blank=True)
  is_active   = models.BooleanField(default=True)
  is_staff    = models.BooleanField(default=True)
  is_admin    = models.BooleanField(default=False)
  date_joined = models.DateTimeField(default=timezone.now)

  objects = MyUserManager()

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = []

  def __str__(self):
    return self.email

  def has_perm(self, perm, obj=None):
    "Does the user have a specific permission?"
    # Simplest possible answer: Yes, always
    return True

  def has_module_perms(self, app_label):
    "Does the user have permissions to view the app `app_label`?"
    # Simplest possible answer: Yes, always
    return True