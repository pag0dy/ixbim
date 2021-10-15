from django.contrib import admin
from .models import User
from .forms import AppUserCreationForm
from django.contrib.auth.admin import UserAdmin

class AppUserAdmin(UserAdmin):
    model = User
    add_form = AppUserCreationForm

# Register your models here.
admin.site.register(User, AppUserAdmin)