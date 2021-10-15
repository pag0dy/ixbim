from django.db import models
import ifcopenshell as IfcOs

#Variables globales
directorio = ''

#Clase que accede al archivo IFC
class IfcDoc(models.Model):
    nombre_archivo = models.FileField()
    uploaded_at = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=False)


    def __str__(self):
        return f"Id del archivo: {self.id}"
