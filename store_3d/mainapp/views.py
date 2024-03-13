import logging

from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import User
from .forms import UserForm, LoginForm, UserProfileForm

logger = logging.getLogger(__name__)

COMMON_CONTENT = settings.COMMON_CONTENT

logger = logging.getLogger(__name__)


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            logger.info(f' Валидация формы успешна')
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                logger.info(f'Пользователь с email: {email} успешно вошел!')
                return redirect('index')
            else:
                logger.error(f"Неудачная попытка входа для пользователя '{email}'. Неверное имя пользователя или пароль.")
                return redirect('register')
    else:
        form = LoginForm()

    content = {
        'form': form,
        'title': 'Вход',
        **COMMON_CONTENT
    }
    logger.debug("Страница входа успешно загружена!")
    return render(request, 'mainapp/login.html', content)


def logout_view(request):
    logout(request)
    logger.info(f'Пользователь успешно вышел!')
    logger.debug("Главная страница успешно загружена!")

    return redirect('index')


def register(request):
    form = UserForm()
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            logger.info(f' Валидация формы успешна')
            user = form.save(commit=False)
            user.password = make_password(form.cleaned_data['password'])
            user.save()
            username = form.cleaned_data.get('username')
            logger.info(f'Пользователь {username} успешно создан')
            return redirect('login')
        else:
            logger.info(f'Ошибка валидации формы: {form.errors}')
    content = {
        'form': form,
        'title': 'Регистрация',
        **COMMON_CONTENT
    }
    logger.debug(f"Страница {content['title']} успешно загружена!")
    return render(request, 'mainapp/register.html', content)


@login_required
def profile(request):
    user = request.user
    content = {
        'user': user,
        'title': 'Страница профиля',
        **COMMON_CONTENT
    }

    return render(request, 'mainapp/profile.html', content)


@login_required
def profile(request):
    user = request.user
    form = UserProfileForm(instance=user)
    content = {
        'form': form,
        'title': 'Страница профиля',
        **COMMON_CONTENT
    }

    return render(request, 'mainapp/profile.html', content)


@login_required
def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user)
        if form.is_valid():
            new_password = form.cleaned_data.get('password')
            if new_password:
                user.set_password(new_password)
            form.save()
            return redirect('profile')
    else:
        form = UserProfileForm(instance=user)
    content = {
        'form': form,
        'title': 'Страница профиля',
        **COMMON_CONTENT
    }
    return render(request, 'mainapp/profile.html', content)


@login_required
def delete_profile(request, user=None):
    if request.method == 'POST':
        user = request.user
        user.delete()
        logout(request)
        return redirect('index')
    content = {
        'user': user,
        'title': 'Страница профиля',
        **COMMON_CONTENT
    }

    return render(request, 'mainapp/profile.html', content)


def index(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            logger.info(f' Валидация формы успешна')
            form.save()

            return redirect('index')

    else:
        form = UserForm()

    content = {
        'form': form,
        'title': 'Главная',

        **COMMON_CONTENT
    }
    logger.debug(f"Страница {content['title']} успешно загружена!")
    return render(request, 'mainapp/index.html', content)


def gallery(request):
    content = {
        'title': 'Галерея',
        **COMMON_CONTENT
    }
    logger.info('successful')
    logger.debug(f"Страница {content['title']} успешно загружена!")
    return render(request, 'mainapp/gallery.html', content)


def contact(request):
    # if request.method == 'POST':
    #     form = MyModelForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         # Можно сделать что-то после успешного сохранения
    #         return redirect('success_url')
    # else:
    #     form = MyModelForm()
    logger.info(f"Index {COMMON_CONTENT['contact']} accessed")
    content = {
        'title': 'Контакты',
        **COMMON_CONTENT
    }

    logger.debug(f"Страница {content['title']} успешно загружена!")
    return render(request, 'mainapp/contact.html', content, )


def about(request):
    logger.debug('About page accessed')
    content = {
        'title': 'О нас',
        **COMMON_CONTENT
    }
    logger.debug(f"Страница {content['title']} успешно загружена!")
    return render(request, 'mainapp/about.html', content)


# ____________________________________________________________Users_____________________________________________________
def user_list(request):
    users = User.objects.all()  # Получение всех пользователей
    context = {
        'users': users,
        'title': 'Список пользователей',  # Заголовок страницы
        **COMMON_CONTENT
    }
    return render(request, 'mainapp/user_list.html', context)


def user_update(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Пользователь успешно обновлен')
            return redirect('user_detail', pk=user.pk)
    else:
        form = UserForm(instance=user)

    context = {
        'form': form,
        'title': 'Редактирование пользователя',
        **COMMON_CONTENT
    }

    return render(request, 'mainapp/user_update.html', context)


def user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    user.delete()
    return redirect('user_list')


def user_detail(request, pk):
    user = get_object_or_404(User, pk=pk)
    return render(request, 'mainapp/profile.html', {'user': user})
