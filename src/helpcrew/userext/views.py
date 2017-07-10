from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth import logout, authenticate, login

from .models import User

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
    if request.method == 'GET':
        return redirect(reverse('user_login'))
    elif request.method == 'POST':
        firstname = request.POST['fname']
        lastname = request.POST['lname']
        username = request.POST['email']
        password = request.POST['password']
        user = User.objects.filter(email=username)
        if not user:
            user = User.objects.create_user(username, password)
            user.firstname = firstname
            user.lastname = lastname
            user.save()
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse('user_profile'))
            else:
                content = {'error': u'Ошибка авторизации'}
                return render(request, 'user/login.html', content)
        else:
            content = {
                'error': u'Электронный адрес уже зарегистрирован в системе',
                'form': {
                    'fname': firstname,
                    'lname': lastname,
                    'email': username
                }
            }
            return render(request, 'user/login.html', content)
