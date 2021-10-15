from django.shortcuts import render, redirect, HttpResponse
from .models import User
from .forms import AppUserCreationForm, ModifyPassForm, ModifyUserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .utils import filtro_usuario
from django.contrib.auth.decorators import login_required
import bcrypt

def user(request):
    return HttpResponse('User')

def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('../analizer/dashboard')      
        else:
            messages.info(request, 'El correo o contraseña ingresados no son correctos')
            return redirect('../')

    
def register(request):
    if request.method == 'POST':
        reg_form = AppUserCreationForm(request.POST)
        if reg_form.is_valid():
            nuevo_usuario=reg_form.save()
            messages.success(request, 'La cuenta ha sido creada!')
            return redirect('loginPage')

        else:   
            print('algo falló')  
            context = {
                'reg_form':reg_form,
            }               
            return render(request, 'master/register.html', context)

    else:
        if request.user.is_authenticated:
            return redirect('../analizer/dashboard')
        else:
            reg_form = AppUserCreationForm()
            context = {
                'reg_form' : reg_form
            }
            return render(request, 'master/register.html', context)

@login_required(login_url='loginPage')
def user_profile(request):
    user = request.user
    context = {
        'user':user,
    }
    return render(request, 'master/user_profile.html', context)


@login_required(login_url='loginPage')
def modify_user(request):
    mod_user_form = request.POST
    if mod_user_form.is_valid():
        user.username = request.POST['username']
        user.email = request.POST['email']
        user.save()
        messages.success(request, 'Tu información de actualizó correctamente!')
        return redirect('dashboard')
    else:
        messages.info(request, 'Los valores ingresados no son válidos.')
        context = {
            'user':user,
        }
        return render(request, 'master/user_profile.html', context)


@login_required(login_url='loginPage')
def modify_pass(request):
    user = request.user
    mod_pass_form = request.POST
    if mod_pass_form.is_valid():
        user.password = request.POST.clean_data('password1')
        user.save()
        messages.success(request, 'Tu contraseña de actualizó correctamente!')
        return redirect('dashboard')
    else:
        messages.info(request, 'Los valores ingresados no son válidos.')
        context = {
            'user':user,
        }
        return render(request, 'master/user_profile.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')
