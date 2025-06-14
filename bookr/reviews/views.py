
from django.shortcuts import render


def index(request):
    return render(request, 'base.html')

def search(request):
    result = request.GET.get('search', 'Введите запрос')
    return render(request, 'search.html', {'result': result})