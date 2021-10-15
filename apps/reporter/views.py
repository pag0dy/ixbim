from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
import io
import xlsxwriter as xr
from .utils import *
from ..analizer.utils import filtro_elemento, filtro_modelo

@login_required(login_url='loginPage')
def reporter(request, id):
    output = io.BytesIO()
    workbook = xr.Workbook(output)
    title = workbook.add_format(
        {'bold': True, 'font_name': 'Roboto', 'font_color': 'white', 'font_size': 28, 'bg_color': '#244155' }
    )
    subtitle = workbook.add_format(
        {'font_name': 'Roboto', 'font_color': 'white', 'font_size': 20, 'bg_color': '#244155'}   
    )
    main_text = workbook.add_format(
        {'font_name': 'Roboto', 'font_color': 'white', 'font_size': 10, 'bg_color': '#244155'}
    )
    bold_text = workbook.add_format(
        {'font_name': 'Roboto', 'font_color': 'white', 'font_size': 10, 'bg_color': '#244155', 'bold': True}
    )
    data_text = workbook.add_format(
        {'font_name': 'Roboto', 'font_color': '#244155', 'font_size': 10, 'align': 'left'}
    )

    portada = workbook.add_worksheet('RESUMEN')
    este_modelo = filtro_modelo(id)

    portada.merge_range('B2:C2', 'Datos del proyecto', subtitle)
    portada.set_column('B:B', 15)
    portada.set_column('C:C', 55)
    portada.write('B3', 'Nombre:', bold_text)
    portada.write('C3', este_modelo.project.name, data_text)
    portada.write('B4', 'Descripción:', bold_text)
    portada.write('C4', este_modelo.project.desc, data_text)
    portada.write('B5', 'Usuario:', bold_text)
    portada.write('C5', este_modelo.project.owner.email, data_text)
    portada.merge_range('B6:C6', 'Datos del modelo', subtitle)
    portada.write('B7', 'Nombre:', bold_text)
    portada.write('C7', este_modelo.name, data_text)
    portada.write('B8', 'Tipología:', bold_text)
    portada.write('C8', este_modelo.model_type, data_text)
    portada.merge_range('B9:C9', 'Información extraida con iX', bold_text)
    model_entities = query_model_elements(este_modelo)
    if model_entities:
        entity_list = list_model_entities(model_entities)
        for e in entity_list:
            new_sheet = workbook.add_worksheet('a.' + str(e))
            new_sheet.set_column('B:B', 10)
            new_sheet.set_column('C:C', 30)
            new_sheet.set_column('D:D', 15)
            new_sheet.set_column('E:E', 115)
            row = 0
            col = 1
            new_sheet.write(row, col, 'ID-IX', bold_text)
            new_sheet.write(row, col+1, 'NOMBRE', bold_text)
            new_sheet.write(row, col+2, 'ATRIBUTO', bold_text)
            new_sheet.write(row, col+3, 'VALOR', bold_text)
            filtered_entities = filter_model_elements(este_modelo, e)
            print(filtered_entities)
            row = 1
            for f in filtered_entities:
                f_attrs = query_element_attrs(f)
                if f_attrs == False:
                    pass
                else:
                    for a in f_attrs:
                        new_sheet.write(row, col, f.id, data_text)
                        new_sheet.write(row, col+1, f.name, data_text)
                        new_sheet.write(row, col+2, a.name, data_text)
                        new_sheet.write(row, col+3, a.value, data_text)
                        row +=1
        for e in entity_list:
            new_sheet = workbook.add_worksheet('p.' + str(e))  
            new_sheet.set_column('B:B', 10)
            new_sheet.set_column('C:C', 30)
            new_sheet.set_column('D:D', 15)
            new_sheet.set_column('E:E', 115)
            row = 0
            col = 1
            new_sheet.write(row, col, 'ID-IX', bold_text)
            new_sheet.write(row, col+1, 'PSET', bold_text)
            new_sheet.write(row, col+2, 'PROPIEDAD', bold_text)
            new_sheet.write(row, col+3, 'VALOR', bold_text)
            filtered_entities = filter_model_elements(este_modelo, e)
            row = 1
            for f in filtered_entities: 
                f_psets = query_element_psets(f) 
                if f_psets == False:
                    pass
                else:    
                    for pst in f_psets:
                        print(pst)
                        f_props = query_pset_properties(pst.id)
                        if f_props:
                            for prop in f_props:
                                new_sheet.write(row, col, f.id, data_text)
                                new_sheet.write(row, col+1, prop.pset.name, data_text)
                                new_sheet.write(row, col+2, prop.name, data_text)
                                new_sheet.write(row, col+3, prop.value, data_text)
                                row +=1
                        else:
                            pass                    


    workbook.close()
    output.seek(0)
    nombre_modelo = str(este_modelo.name)
    nombre_reporte = nombre_modelo.replace(" ", "_")
    filename = nombre_reporte + '.xlsx'
    response =HttpResponse(
            output,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
    response['Content-Disposition'] = 'attachment; filename=%s' % filename

    return response


