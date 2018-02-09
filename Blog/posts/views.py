from django.http import HttpResponse
from django.shortcuts import render
from .models import Post


def home(request):
    title = 'Test'
    return render(request, 'index.html', {'title': title})
