from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth import logout, authenticate, login

def user_profile(request):
    content = {}
    return render(request, 'user/profile.html', content)


def user_login(request):
    if request.method == 'GET':
        return render(request, 'user/login.html', {})
    elif request.method == 'POST':
        username = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(reverse('user_profile'))
        else:
            return redirect(reverse('user_login'))


def user_logout(request):
    logout(request)
    return redirect('/')


def user_register(request):
    content = {}
    return render(request, 'user/register.html', content)
