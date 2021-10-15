from ..analizer.models import Attribute, Elemento, IfcModel, Property, Pset
import xlsxwriter as wr
from ..master.models import *
import datetime
import time

def filter_ifcModel(id_ifcModel):
    active = IfcModel.objects.filer(id = id_ifcModel)
    if active:
        this_ifcModel = active[0]
        return this_ifcModel
    else:
        mensaje = 'No se encontró el modelo'
        print(mensaje)
        return mensaje

def filter_project(id_project):
    active = Project.objects.filter(id = id_project)
    if active:
        this_project = active[0]
        return this_project
    else:
        mensaje = 'No se encontró el proyecto'
        print(mensaje)
        return(mensaje)

def query_model_elements(ifcModel):
    has_elements = Elemento.objects.filter(ifcModel = ifcModel)
    if has_elements:
        model_elements = has_elements
        return model_elements
    else:
        return False

def filter_model_elements(ifcModel, ifcEntity):
    entity_filter = Elemento.objects.filter(ifcModel = ifcModel, ifcEntity = ifcEntity)
    return entity_filter

def list_model_entities(model_elements):
    entity_list = []
    for e in model_elements:
        if e.ifcEntity in entity_list:
            pass
        else:
            entity_list.append(e.ifcEntity)

    return entity_list

def query_element_attrs(element):
    has_attrs = Attribute.objects.filter(element = element)
    if has_attrs:
        element_attrs = has_attrs
        return element_attrs
    else:
        return False

def query_element_psets(element):
    has_psets = Pset.objects.filter(element = element)
    if has_psets:
        element_psets = has_psets
        return element_psets
    else:
        return False

def query_elements_qset(id_element):
    pass

def query_pset_properties(pset):
    has_properties = Property.objects.filter(pset = pset)
    if has_properties:
        pset_properties = has_properties
        return pset_properties
    else:
        return False

def query_elementos_quantities(id_element):
    pass

def fecha_reporte():
    fecha = datetime.date.today()
    t = time.localtime()
    hora = time.strftime("%H:%M:%S", t)
    creado_en = str(fecha) + ' ' + str(hora)
    return creado_en

