from django import forms
from django.forms import fields
from .models import Project
from ..user.validators import letters_only, confirm_pass
from django.core.exceptions import ValidationError

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ['owner']