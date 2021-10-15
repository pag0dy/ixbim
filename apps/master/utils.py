from .models import *

def filter_project(project_id):
    project = Project.objects.filter(id=project_id)
    if project:
        this_project = project[0]
        return this_project
    else:
        mensaje = 'No se encontró el elemento'
        print(mensaje)
        return False