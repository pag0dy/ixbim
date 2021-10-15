from django.urls import path
from . import views

urlpatterns = [
    path('', views.analizer, name = 'analizer'),
    path('ifcquery/<int:id>', views.ifcquery, name= 'ifcquery'),
    path('dashboard', views.dashboard, name= 'dashboard'),
    path('datadash/<int:id>', views.datadash, name = 'datadash'),
    path('element_detail/<int:id>', views.element_detail, name= 'element_detail')
]
