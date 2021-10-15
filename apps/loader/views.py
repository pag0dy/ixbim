from ..master.models import Project
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from .forms import IfcUploadForm
from .models import IfcDoc
import ifcopenshell as IfcOs
import ifcopenshell.util
import ifcopenshell.util.element
import os.path
from pathlib import Path
from django.core.files.storage import FileSystemStorage
from .utils import filtro_archivo
from ..user.utils import filtro_usuario
from ..reporter.utils import filter_project

@login_required(login_url='loginPage')
def loader(request, project):
    if request.method == 'POST':
        form = IfcUploadForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            obj = form.save()
            request.session['file_id'] = obj.id
            return redirect('loaded')
    else:
        form = IfcUploadForm(request.POST or None, request.FILES or None)
        user = request.user
        this_project = filter_project(project)
        request.session['current_project_id'] =  project
        context = {
            'user': user,
            'form': form,
            'project':this_project,
        }
        return render(request, 'loader/loader.html', context)


@login_required(login_url='loginPage')
def loaded(request):
    if 'current_project_id' in request.session:
        if request.method == 'GET':
            this_project = filter_project(request.session['current_project_id'])
            Ifc_file = filtro_archivo(request.session['file_id'])
            with open(Ifc_file.nombre_archivo.path, 'r') as f:
                doc = IfcOs.open(Ifc_file.nombre_archivo.path)
                proy = doc.by_type('IfcProject')[0]
                proyecto = proy.Name
                esquema = doc.schema
                edi = doc.by_type('IfcBuilding')[0]
                edificio = edi.Name
                apli = doc.by_type('IfcApplication')[0]
                aplicacion = apli.ApplicationFullName
            context = {
                'db_project': this_project,
                'proyecto': proyecto,
                'esquema': esquema,
                'edificio': edificio,
                'aplicacion': aplicacion,
            }

            return render(request, 'loader/loaded.html', context=context)

