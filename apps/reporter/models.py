from django.db import models
from django.db.models.fields.related import ForeignKey
from ..analizer.models import IfcModel

class ModelReport(models.Model):
    url = models.FileField(upload_to="reports/")
    ifcModel = models.OneToOneField(IfcModel, related_name="report", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    # def __str__(self):
    #     return self.url