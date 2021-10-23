from django.urls import path
from . import views

urlpatterns = [
    path('', views.reporter, name = 'reporter'),
    path('downloadReport/<int:id>', views.downloadReport, name= 'downloadReport'),
]
