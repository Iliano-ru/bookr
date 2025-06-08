from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    name = request.GET.get('name', '')
    # name = request.GET.get('name') or ''
    return HttpResponse("hi " + name)