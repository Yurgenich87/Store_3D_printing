import logging

from django import forms
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .forms import MyModelForm
from store_3d.settings import common_content

logger = logging.getLogger(__name__)


def index(request):
    logger.info('Index page accessed')
    if request.method == 'POST':
        form = MyModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success_url')
    else:
        form = MyModelForm()
    content = {
        'title': 'Главная',
        **common_content
    }

    return render(request, 'mainapp/index.html', content)


def contact(request):
    # if request.method == 'POST':
    #     form = MyModelForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         # Можно сделать что-то после успешного сохранения
    #         return redirect('success_url')
    # else:
    #     form = MyModelForm()
    logger.info(f"Index {common_content['contact']} accessed")
    content = {
        'title': 'Контакты',
        **common_content
    }
    return render(request, 'mainapp/contact.html', content,)


def about(request):
    logger.debug('About page accessed')
    content = {
        'title': 'О нас',
        **common_content
    }

    return render(request, 'mainapp/about.html', content)


def home(request):
    return render(request, 'mainapp/home.html')




