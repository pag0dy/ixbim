from django.core import validators
from django.db import models
from django.contrib import messages
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator, RegexValidator, validate_slug, EmailValidator
import bcrypt

class User(AbstractUser):
    empresa = models.CharField(max_length=100, validators= [MinLengthValidator(limit_value=2, message = 'El nombre de la empresa debe tener al menos dos caracteres')])
    REQUIRED_FIELDS = ['email', 'password']

    def __str__(self):
        return self.username