from django import forms
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm

from django.forms import fields, widgets
from .models import User
from .validators import letters_only, confirm_pass
from django.core.exceptions import ValidationError

class AppUserCreationForm(UserCreationForm):
    password1 = forms.CharField(
        label= 'Contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        label= 'Confirma tu contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    class Meta:
        model = User
        fields = ['username','email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'helptext': None,
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control'
            }),

        }
        help_text = {
            'username': None,
            'email': None,
            'password1': None,
            'password2': None,
        }
        labels = {
            'username': 'Usuario',
            'email': 'Email'
        }


class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'password']

        widgets = {
            'password': forms.PasswordInput()
        }

        labels = {
            'password': 'Contraseña'
        }

class ModifyUserForm(forms.ModelForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
        }),
        error_messages={'invalid': 'Por favor ingrese un email válido'}
    )
    name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        })
    )
    class Meta:
        model = User
        fields = ['name', 'email']

        labels = {
            'name': 'Nombre de usuario'
        }

class ModifyPassForm(forms.ModelForm):
    confirmpass = forms.CharField(max_length=80, label='Confirmar contraseña', widget= forms.PasswordInput(attrs={
        'class':'form-control'
    }))
    widgets = {
        'confirmpass' : forms.PasswordInput()
    }

    class Meta:
        model = User
        fields = ['password']

        widgets = {
        'password' : forms.PasswordInput(attrs={
           'class':'form-control' 
        })
        }

        labels = {
            'password': 'Contraseña',
        }

    def clean_password(self):
        data = self.cleaned_data['password']
        confirm =  self.data['confirmpass']
        errors = []
        errors.append(confirm_pass(data, confirm))
        if errors == [None]:
            return data
        else:
            raise ValidationError(errors)