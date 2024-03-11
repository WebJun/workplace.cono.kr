from django.shortcuts import render
from create_logger import create_logger
from django.http import HttpResponse

logger = create_logger('views_front')


def index(request):
    with open('public_key.pem', 'r') as file:
        public_key = file.read()
    context = {'public_key': public_key}
    return render(request, 'workplace/index.html', context)


def members_login_success(request):
    return render(request, 'workplace/members_login_success.html')


def favicon(request):
    favicon_path = './static/favicon.ico'
    with open(favicon_path, 'rb') as f:
        response = HttpResponse(f.read(), content_type='image/x-icon')
    return response
