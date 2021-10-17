from os import error
from .models import *
import ifcopenshell as IfcOs
import ifcopenshell.util
import ifcopenshell.util.element

def filtro_modelo(id_modelo):
    modelo = IfcModel.objects.filter(id = id_modelo)
    if modelo:
        este_modelo = modelo[0]
        return este_modelo
    else:
        mensaje = 'No se encontró el modelo'
        print(mensaje)
        return mensaje

def filtro_elemento(id_elemento):
    elemento = Elemento.objects.filter(id = id_elemento)
    if elemento:
        este_elemento = elemento[0]
        return este_elemento
    else:
        mensaje = 'No se encontró el elemento'
        print(mensaje)
        return mensaje    

def filtro_elemento_entidad(entidad, element_qs):
    elementos = element_qs.filter(ifcEntity = entidad)
    if elementos:
        return elementos
    else:
        mensaje = 'No se encontró esta entidad en el modelo'
        print(mensaje)
        return mensaje  

def filtro_elemento_atributo(atributo, element_qs):
    elementos = element_qs.attributes.filter(name=atributo)
    if elementos:
        return elementos
    else:
        mensaje = 'No se encontró esta entidad en el modelo'
        print(mensaje)
        return mensaje  

def replace_null(tup):
    lst = list(tup)
    if lst[1] == None:
        lst[1] = "Sin información"
    tup = tuple(lst)
    return tup

def get_element_material(elemento):
    materials = []
    try:
        associations = elemento.HasAssociations
        if associations:
            for a in associations:
                print(a.is_a())
                if a.is_a() == 'IfcRelAssociatesMaterial':
                    a_material = a.RelatingMaterial
                    print(a_material.is_a())
                    if a_material.is_a() == 'IfcMaterialLayerSetUsage':
                        a_layers = a_material.ForLayerSet.MaterialLayers
                        for layer in a_layers:
                            materials.append(layer.Material.Name)                    
                        # a_layers = a_material.ForLayerSet.LayerSetName
                        # materials.append(a_layers)
                    elif a_material.is_a() == 'IfcMaterialProfileSet':
                        a_profiles = a_material.MaterialProfiles
                        for profile in a_profiles:
                            materials.append(profile.Material.Name)
                    elif a_material.is_a() == 'IfcMaterialConstituentSet':
                        a_constituents = a_material.MaterialConstituents
                        for constituent in a_constituents:
                            if constituent.Material.Name in materials:
                                pass
                            else:
                                materials.append(constituent.Material.Name)
                    elif a_material.is_a() == 'IfcMaterial':

                        materials.append(a_material.Material.Name)
                    else:
                        pass
    except:
        materials.append('Sin información') 
    
    print(materials)
    return materials

def get_space_level(espacio):
    space_level = ''
    try:
        decomposes =espacio.Decomposes
        if decomposes.is_a() == 'IfcRelAggregates':
            for d in decomposes:
                if d.RelatingObject.is_a() == 'IfcBuildingStorey':
                    space_level = d.RelatingObject.Name
                else:
                    pass
    except:
            space_level = 'Sin Información'

    return space_level

def get_space_zone(espacio):
    space_zone = ''
    try:
        group = espacio.HasAssignments
        if group:
            for g in group:
                if g.is_a() == 'IfcRelAssignsToGroup':
                    space_zone = str(g.RelatingGroup.Name) + ' - ' + str(g.RelatingGroup.LongName)
                else:
                    pass
    except:
        space_zone = 'Sin Información'
    return space_zone

def get_element_level(elemento):
    element_level = ''
    try:
        contained_in = elemento.ContainedInStructure
        for c in contained_in:
            if c.RelatingStructure.is_a() == 'IfcBuildingStorey':
                element_level = str(c.RelatingStructure.Name) + ' - ' + str(c.RelatingStructure.LongName)
        else:
            pass
    except:
        element_level = 'Sin Información'

    return element_level

def get_element_space(elemento):
    element_space = ''
    try:
        contained_in = elemento.ContainedInStructure
        for c in contained_in:
            if c.RelatingStructure.is_a() == 'IfcSpace':
                element_space = str(c.RelatingStructure.Name) + ' - ' + str(c.RelatingStructure.LongName)
        else:
            pass
    except:
        element_space = 'Sin Información'

    return element_space

def get_classification(elemento):
    element_classification = ''
    try:
        associations = elemento.HasAssociations
        if associations:
            for a in associations:
                if a.is_a() == 'IfcRelAssociatesClassification':
                    a_classification = a.RelatingClassification.Name
                    a_classification_code = a.RelatingClassification.Identification
                    element_classification = str(a_classification_code) + ' - ' + str(a_classification)

    except:
        element_classification = 'Sin Información'
        return element_classification

    return element_classification

def get_all_objects(doc):
    entis = doc.by_type('IfcObject')
    return entis

