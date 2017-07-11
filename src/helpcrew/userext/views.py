from django.core.files import File
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth import logout, authenticate, login
import os

from .models import User
from ..settings import UPLOAD_DIR

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


def user_activate(request):
    if request.method == 'GET':
        return redirect(reverse('user_profile'))
    elif request.method == 'POST':
        code = request.POST['code']
        user = User.objects.filter(uuid=code)
        if not user:
            content = {'error': u'Ошибка активации'}
            return render(request, 'user/profile.html', content)
        else:
            if user[0].email == request.user.email:
                user[0].is_checked = True
                user[0].save()
                request.user.is_checked = True
                return render(request, 'user/profile.html', {})
            else:
                content = {'error': u'Ошибка активации'}
                return render(request, 'user/profile.html', content)


def user_save(request):
    if request.method == 'GET':
        return redirect(reverse('user_profile'))
    elif request.method == 'POST':
        user = User.objects.filter(email=request.user.email)
        user = user[0]
        if not user:
            content = {'error': u'Пользователь не найден'}
            return render(request, 'user/profile.html', content)
        else:
            if 'avatar' in request.FILES:
                up_file = request.FILES['avatar']
                file = os.path.join(UPLOAD_DIR, User.avatar_path(user, up_file.name))
                filename = os.path.basename(file)
                destination = open(file, 'wb+')
                for chunk in up_file.chunks():
                    destination.write(chunk)
                user.avatar.save(filename, destination, save=False)
                destination.close()

            firstname = request.POST['fname']
            lastname = request.POST['lname']
            user.firstname = firstname
            user.lastname = lastname
            user.save()

            return redirect(reverse('user_profile'))
