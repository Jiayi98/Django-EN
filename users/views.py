"""
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import authenticate, login
from .forms import UserRegisterForm, LoginForm

# create your views here.

def register(request):
    if request.method == 'post':
        form = UserRegisterForm(request.post)
        if form.is_valid():
            form.save()

            # username can be changed to email address
            username = form.cleaned_data.get('username')
            # username can be changed to email address
            messages.success(request, f'account created for {username} and you are able to log in!')
            # part6(https://www.youtube.com/watch?v=q4jpr-m0taq&list=pl-osie80tettoqckz03tu5fnfx2uy6u4p&index=6) 26:00
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html',{'form': form})

# @permission_required('appname.can_browse_monitor', login_url="/login/")

def user_login(request):
    if request.method == 'post':
        form = LoginForm(request.post)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                return HttpResponse('authenticated successfully')
            else:
                return HttpResponse('disabled account')
        else:
            return HttpResponse('invalid login')
    else:
        form = LoginForm()

    return render(request, 'users/login.html', {'form':form})

@login_required
def dashboard(request):
    return render(request, 'users/dashboard.html', {'section':'dashboard'})

@login_required
def user_logout(request):
    return render(request, 'users/logout.html')

"""

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def dashboard(request):
    return render(request, 'users/dashboard.html')



