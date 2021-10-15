from django.core.exceptions import ValidationError
from .models import User

def filtro_usuario_email(email):
    activo = User.objects.filter(email = email)
    if activo:
        usuario_activo = activo[0]
        return usuario_activo

def confirm_pass(pass1, pass2):
    if pass1 == pass2:
        pass_confirmed = pass1
        pass
    else:
        raise ValidationError('Las contraseñas ingresadas no coinciden')


def letters_only(string):
    if str.isalpha(string):
        string_passed = string
        return string_passed
    else:
        raise ValidationError('Este campo debe contener sólo letras')


