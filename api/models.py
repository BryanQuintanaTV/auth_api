from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from  django.contrib.auth.models import PermissionsMixin
from django.db import models
import bcrypt

# Create your models here.
# User management class
class UserManager(BaseUserManager):

    # Method to create users in base of user model config
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email Field Must Be Set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    # Method to create a default user (SuperUser)
    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, email, password, **extra_fields)

# User Model that contains the table's config in the db
class User(AbstractBaseUser, PermissionsMixin):
    # Columns where we store the most important data of the user
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)

    # Columns for auth and use of the Users API
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # Auth configuration based on Django Docs
    objects = UserManager()

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']

    # Method for hashing the password
    def set_password(self, raw_password):
        self.password = bcrypt.hashpw(raw_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    # Method that verify if the given password coincide with the hash
    def check_password(self, raw_password):
        return bcrypt.checkpw(raw_password.encode('utf-8'), self.password.encode('utf-8'))

    # Method that returns the username
    def __str__(self):
        return self.username