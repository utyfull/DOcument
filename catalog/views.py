from django.shortcuts import render
from django.shortcuts import render
from .models import Book


def home_page(request):
    # получаем все значения модели
    data = Book.objects.all()
    return render(request, 'home_page.html', {'data': data})
# Create your views here.
