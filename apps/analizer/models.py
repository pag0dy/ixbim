from ..master.models import Project
from django.db import models
from django.contrib import messages
from django.core.validators import MinLengthValidator, RegexValidator, validate_slug, EmailValidator
from ..master.models import Project
import bcrypt

class IfcModel(models.Model):
    MODEL_TYPE = (
        ('ARQ', 'Arquitectura'),
        ('SIT', 'Sitio'),
        ('VOL', 'Volumen'),
        ('EST', 'Estructura'),
        ('MEP', 'MEP'),
        ('COR', 'Coodrindación'),
        ('CON', 'Construcción'),
        ('ASB', 'As-Built'),
        ('OPE', 'Operación')
    )
    name = models.CharField(max_length=100, validators = [MinLengthValidator(limit_value = 2, message = 'El nombre debe tener más de dos caracteres')])
    project = models.ForeignKey(Project, related_name='models', on_delete=models.CASCADE, null =True)
    model_type = models.CharField(max_length=3, choices=MODEL_TYPE, default='ARQ')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Elemento(models.Model):
    name = models.CharField(max_length=255)
    ifcEntity = models.CharField(max_length=255)
    ifcModel = models.ForeignKey(IfcModel, related_name='entities', on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

class Attribute(models.Model):
    name = models.CharField(max_length=255)
    value = models.CharField(max_length=255)
    element = models.ForeignKey(Elemento, related_name='attributes', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Pset(models.Model):
    name = models.CharField(max_length=255)
    element = models.ForeignKey(Elemento, related_name='psets', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Property(models.Model):
    name = models.CharField(max_length=255)
    value = models.CharField(max_length=255)
    pset = models.ForeignKey(Pset, related_name='properties', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Qto(models.Model):
    name = models.CharField(max_length=255)
    measure = models.CharField(max_length=255)
    element = models.OneToOneField(Elemento, related_name='qto', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Measure(models.Model):
    name = models.CharField(max_length=255)
    value = models.CharField(max_length=255)
    qto = models.ForeignKey(Qto, related_name='measures', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)