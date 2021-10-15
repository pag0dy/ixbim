from apps.analizer.models import IfcModel
from apps.analizer.utils import filtro_modelo
from apps.master.utils import filter_project
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Project
from .utils import filter_project
from .forms import ProjectForm
from ..user.utils import filtro_usuario


def home(request):
    return render(request, 'master/home.html')

def error(request):
    return render(request, 'master/error.html')

def permission_error(request):
    return render(request, 'master/permission_error.html')

@login_required(login_url='loginPage')
def new_project(request):
    user =request.user
    if request.method == 'POST':
        this_project = Project.objects.create(name=request.POST['project_name'], desc=request.POST['project_desc'], owner=user)
        return redirect('dashboard')
    else:
        return render(request, 'master/new_project.html')


@login_required(login_url='loginPage')
def project_managment(request, id):
    user = request.user
    this_project = filter_project(project_id=id)
    project_models = IfcModel.objects.filter(project=this_project)
    context = {
        'project': this_project,
        'usuario': user,
        'models': project_models,
    }
    return render(request, 'master/project_management.html', context)


@login_required(login_url='loginPage')
def modify_project(request, id):
    if request.method == 'POST':
        user = request.user
        this_project = filter_project(project_id=id)
        this_project.name = request.POST['project_name']
        this_project.desc = request.POST['project_desc']
        this_project.save()
        return redirect('dashboard')

@login_required(login_url='loginPage')
def modify_model(request, id):
    if request.method == 'POST':
        user = request.user
        this_model = filtro_modelo(id_modelo=id)
        this_model.name = request.POST['model_name']
        this_model.model_type = request.POST['model_type']
        this_model.save()
        return redirect('dashboard')
    else:
        return redirect('error')

@login_required(login_url='loginPage')
def delete_model(request, id):
    user = request.user
    modelo = filtro_modelo(id_modelo=id)
    if modelo:
        modelo.delete()
        return redirect('dashboard')

    else:
        return redirect('error')

@login_required(login_url='loginPage')
def delete_project(request, id):
    user = request.user
    this_project = filter_project(project_id=id)
    if this_project:
        this_project.delete()
        return redirect('dashboard')