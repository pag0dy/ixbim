from django.contrib import admin
from .models import IfcModel, Elemento, Property, Pset, Qto, Measure, Attribute

admin.site.register(IfcModel)
admin.site.register(Elemento)
admin.site.register(Pset)
admin.site.register(Property)
admin.site.register(Qto)
admin.site.register(Measure)
admin.site.register(Attribute)
