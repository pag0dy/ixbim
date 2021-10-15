from django.db.models import fields
import django_filters
from ifcopenshell.ifcopenshell_wrapper import attribute
from .models import *
from django.db.models import Q

class ElementFilter(django_filters.FilterSet):
    ifcEntity = django_filters.CharFilter(label="Entidad IFC", lookup_expr='iexact')
    attributes__name = django_filters.CharFilter(label="Atributo", lookup_expr='iexact')
    attributes__value = django_filters.CharFilter(label="Valor del atributo", lookup_expr='iexact')
    psets__name = django_filters.CharFilter(label="Pset", lookup_expr='iexact')
    psets__properties__name =django_filters.CharFilter(label="Propiedad", lookup_expr='iexact', distinct=True)
    psets__properties__value = django_filters.CharFilter(label="Valor de la propiedad", lookup_expr='iexact', distinct=True)

    class Meta:
        model = Elemento
        fields = ['id', 'ifcEntity']

        
        