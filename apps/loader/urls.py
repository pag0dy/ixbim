from django.urls import path
from . import views

urlpatterns = [
    path('<int:project>', views.loader, name = 'loader'),
    path('loaded', views.loaded, name = 'loaded'),
]
