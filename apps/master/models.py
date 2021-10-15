from django.db import models
from django.contrib import messages
from django.core.validators import MinLengthValidator, RegexValidator, validate_slug, EmailValidator
from ..user.models import User
import bcrypt

class Project(models.Model):
    name = models.CharField(max_length=100, validators = [MinLengthValidator(limit_value = 2, message = 'El nombre debe tener más de dos caracteres')])
    desc = models.CharField(max_length=255)
    owner = models.ForeignKey(User, related_name='projects_created', on_delete=models.CASCADE, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name