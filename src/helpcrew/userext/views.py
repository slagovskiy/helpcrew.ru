from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth import logout, authenticate, login
from django.template.loader import render_to_string
from django.contrib import messages
import os

from .models import User
from .decoretors import authenticate_check
from ..settings import UPLOAD_DIR
from ..taskqueue.utils import add_email
from ..helpdesk.models import Crew, CrewUsers


@authenticate_check
def user_profile(request):
    crews_a = Crew.objects.filter(
        id__in=CrewUsers.objects.filter(user=request.user, type=CrewUsers.ADMINISTRATOR_TYPE).values_list('crew', flat=True)
    )
    crews_d = Crew.objects.filter(
        id__in=CrewUsers.objects.filter(user=request.user, type=CrewUsers.DISPATCHER_TYPE).values_list('crew', flat=True)
    )
    crews_o = Crew.objects.filter(
        id__in=CrewUsers.objects.filter(user=request.user, type=CrewUsers.OPERATOR_TYPE).values_list('crew', flat=True)
    )
    content = {
        'crews':
            {
                'crews_a': crews_a,
                'crews_d': crews_d,
                'crews_o': crews_o
            }
        }
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
                add_email(
                    msg_to=user.email,
                    subject=u'Код подтверждения регистрации',
                    body=render_to_string('user/email_register.html', {'user': user})
                )
                return redirect(reverse('user_profile'))
            else:
                messages.error(request, u'Ошибка авторизации')
                return render(request, 'user/login.html', {})
        else:
            messages.error(request, u'Электронный адрес уже зарегистрирован в системе')
            content = {
                'form': {
                    'fname': firstname,
                    'lname': lastname,
                    'email': username
                }
            }
            return render(request, 'user/login.html', content)


@authenticate_check
def user_activate(request):
    if request.method == 'GET':
        return redirect(reverse('user_profile'))
    elif request.method == 'POST':
        code = request.POST['code']
        user = User.objects.filter(uuid=code)
        if not user:
            messages.error(request, u'Ошибка активации')
            return render(request, 'user/profile.html', {})
        else:
            if user[0].email == request.user.email:
                user[0].is_checked = True
                user[0].save()
                request.user.is_checked = True
                return render(request, 'user/profile.html', {})
            else:
                messages.error(request, u'Ошибка активации')
                return render(request, 'user/profile.html', {})


def user_save(request):
    if request.method == 'GET':
        return redirect(reverse('user_profile'))
    elif request.method == 'POST':
        user = User.objects.filter(email=request.user.email)
        user = user[0]
        if not user:
            messages.error(request, u'Пользователь не найден')
            return render(request, 'user/profile.html', {})
        else:
            try:
                if request.POST['type'] == 'info':
                    if 'avatar' in request.FILES:
                        up_file = request.FILES['avatar']
                        file = os.path.join(UPLOAD_DIR, User.avatar_path(user, up_file.name))
                        filename = os.path.basename(file)
                        if not os.path.exists(os.path.dirname(file)):
                            os.makedirs(os.path.dirname(file))
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
                elif request.POST['type'] == 'password':
                    password1 = request.POST['password1']
                    password2 = request.POST['password2']
                    if password1 == password2:
                        user.set_password(password1)
                        user.save()
                        user = authenticate(request, username=user.email, password=password1)
                        if user is not None:
                            login(request, user)
                            add_email(
                                msg_to=user.email,
                                subject=u'Изменение пароля',
                                body=render_to_string('user/email_password.html', {'user': user})
                            )
                    else:
                        messages.error(request, u'Пароли не совпадают')
                        return render(request, 'user/profile.html', {})
                    return redirect(reverse('user_profile'))
                else:
                    return redirect(reverse('user_profile'))
            except:
                messages.error(request, u'Ошибка сохранения')
                return render(request, 'user/profile.html', {})
