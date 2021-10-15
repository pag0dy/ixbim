from ..reporter.utils import filter_project
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
import ifcopenshell as IfcOs
import ifcopenshell.util
import ifcopenshell.util.element
from itertools import chain
from ..loader.utils import filtro_archivo
from .models import IfcModel, Elemento, Attribute, Pset, Property
from ..master.models import Project
from .utils import filtro_elemento, filtro_elemento_entidad, filtro_elemento_atributo , get_element_material, replace_null, filtro_modelo, get_element_space, get_element_level, get_space_level, get_space_zone, get_classification
from .filters import ElementFilter

@login_required(login_url='loginPage')
def analizer(request):
    if request.method == 'POST':
        if 'current_project_id' in request.session:
            this_project = filter_project(request.session['current_project_id'])
            if 'file_id' in request.session:
                Ifc_file = filtro_archivo(request.session['file_id'])
                this_model = IfcModel.objects.create(name=request.POST['modelName'], project=this_project, model_type=request.POST['modelType'])
                request.session['id_modelo'] = this_model.id
                with open(Ifc_file.nombre_archivo.path, 'r') as f:
                    doc = IfcOs.open(Ifc_file.nombre_archivo.path)
                    entis = doc.by_type('IfcObject')
                    proyecto = doc.by_type('IfcProject')
                    entidades = chain(proyecto, entis)
                    abstractas = ['IfcProject', 'IfcBuilding', 'IfcBuildingStorey', 'IfcSite', 'IfcGroup', 'IfcZone']

                    for en in entidades:
                        print('ingresando ' + str(en.is_a()) + '...')
                        try:
                            el = Elemento.objects.create(name=en.Name, ifcEntity=en.is_a(), ifcModel = this_model)
                            e_class = get_classification(en)
                            if e_class == '':
                                e_class='Sin información'
                            else:
                                pass
                            print(e_class)
                            Attribute.objects.create(name='Clasificación', value=e_class, element=el)
                            if en.is_a() in abstractas:
                                pass         
                            elif en.is_a() == 'IfcSpace':
                                s_level = get_space_level(en)
                                Attribute.objects.create(name='Nivel', value=s_level, element=el)
                                s_zone = get_space_zone(en)
                                Attribute.objects.create(name='Zona', value= s_zone, element=el)
                            else:
                                e_material = str(get_element_material(en)).translate({ ord(c): None for c in "[]" })
                                e_material = e_material[:254]
                                if e_material:
                                    print(e_material)
                                    Attribute.objects.create(name='Material', value=e_material, element=el)
                                else:
                                    pass
                                e_level = str(get_element_level(en))
                                if e_level:
                                    print(e_level)
                                    Attribute.objects.create(name='Nivel', value=e_level, element=el)
                                else:
                                    pass
                                e_space = str(get_element_space(en))
                                if e_space:
                                    print(e_space)
                                    Attribute.objects.create(name='Espacio', value=e_space, element=el)
                                else:
                                    pass
                            
                            atts = en.get_info()
                            for item in atts.items():
                                print("ingresando atributos...")
                                item = replace_null(item)
                                Attribute.objects.create(name=item[0], value=item[1], element=el)
                            
                            
                            psets = ifcopenshell.util.element.get_psets(en)
                            for key, value in psets.items():
                                print("ingresando psets...")
                                propset = Pset.objects.create(name=key, element=el)
                                props = value
                                for key, value in props.items():
                                    print("ingresando propiedades...")
                                    Property.objects.create(name=key, value=value, pset=propset)
                        except ValueError:
                            print('ups... algo falló')
            else:
                return redirect('error')

        else:
            return redirect('error')

        print("limpiando base de datos...")
        Ifc_file.delete()
        
        return redirect('dashboard')

    else:
        return redirect('error')


@login_required(login_url='loginPage')
def ifcquery(request, id):
    dic_entidades = {}
    este_modelo = filtro_modelo(id)
    if este_modelo:
        elementos_modelo = este_modelo.entities.all()
        filtro_ifc = ElementFilter(request.GET, queryset=elementos_modelo)
        elementos_modelo = filtro_ifc.qs
        context = {
            'modelo': este_modelo,
            'filtro_ifc':filtro_ifc,
            'elementos_modelo':elementos_modelo,
        }
        return render(request, 'analizer/ifcquery.html', context)
    else:
        return redirect('error')


@login_required(login_url='loginPage')
def dashboard(request):
    sus_proyectos = Project.objects.filter(owner = request.user)
    context = {
        'usuario': request.user,
        'proyectos': sus_proyectos,
    }
    return render(request, 'analizer/dashboard.html', context)

@login_required(login_url='loginPage')
def datadash(request, id):
    este_modelo = filtro_modelo(id)
    if este_modelo:
        elementos_modelo = este_modelo.entities.all()
        niveles_ifc = filtro_elemento_entidad('IfcBuildingStorey', elementos_modelo)
        espacios_ifc = filtro_elemento_entidad('IfcSpace', elementos_modelo)


        # if proyecto_ifc:
        #     este_proyecto_ifc = proyecto_ifc[0]
        #     proyecto_ifc_longname = este_proyecto_ifc.attributes.get(name = 'LongName')
        #     proyecto_ifc_desc = este_proyecto_ifc.attributes.get(name = 'Description')
        # sitio_ifc = filtro_elemento_entidad('IfcSite', elementos_modelo)
        # if sitio_ifc:
        #     este_sitio = sitio_ifc[0]
        #     sitio_composition = este_sitio.attributes.get(name='CompositionType')
        #     sitio_lat = este_sitio.attributes.get(name='RefLatitud')
        #     sitio_lon = este_sitio.attributes.get(name='RefLongitud')
        #     sitio_ele = este_sitio.attributes.get(name='RefElevation')
        #     sitio_title_num = este_sitio.attributes.get(name='LandTitleNumber')
        #     sitio_addr = este_sitio.attributes.get(name='SiteAddress')
        # edif_ifc = filtro_elemento_entidad('IfcBuilding', elementos_modelo)
        # if edif_ifc:
        #     este_edif = edif_ifc[0]
        #     edif_longname = este_edif.attributes.get(name='LongName')
        #     edif_desc = este_edif.attributes.get(name='Description')
        #     edif_composition = este_edif.attributes.get(name='CompositionType')
        #     edif_addr = este_edif.attributes.get(name='BuildingAddress')


            


    context = {
        'modelo': este_modelo,
        'niveles': niveles_ifc,
        'espacios': espacios_ifc
    }
    return render(request, 'analizer/datadash.html', context)

@login_required(login_url='loginPage')
def element_detail(request, id):
    elemento = filtro_elemento(id_elemento=id)
    if elemento:
        atributos = elemento.attributes.all()
        psets = elemento.psets.all()
    context = {
        'elemento':elemento,
        'atributos':atributos,
        'psets':psets

    }
    return render(request, 'analizer/element_detail.html', context)


