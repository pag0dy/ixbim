from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('error', views.error, name= 'error'),
    path('permission_error', views.permission_error, name= 'permission_error'),
    path('new_project', views.new_project, name='new_project'),
    path('project_management/<int:id>', views.project_managment, name='project_management'),
    path('modify_project/<int:id>', views.modify_project, name='modify_project'),
    path('modify_model/<int:id>', views.modify_model, name='modify_model'),
    path('delete_model/<int:id>', views.delete_model, name='delete_model'),
    path('delete_project/<int:id>', views.delete_project, name='delete_project'),
]
