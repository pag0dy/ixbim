from django import forms
from .models import IfcDoc

class IfcUploadForm(forms.ModelForm):
    nombre_archivo = forms.FileField(label="", widget=forms.FileInput(attrs={
        'class': 'form-control',
    }))

    class Meta:
        model = IfcDoc
        fields = ('nombre_archivo',)


