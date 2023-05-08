from django.shortcuts import render

from catalog.models import Category, Product


# Create your views here.

def index(request):
    context = {
        'object_list': Product.objects.all,
        'category_list': Category.objects.all
    }
    return render(request, 'catalog/index.html', context)


def contacts(request):
    return render(request, 'catalog/contacts.html')


def card(request, pk):
    product = Product.objects.get(pk=pk)
    context = {
        'object': product,
        'title': product.name
    }
    return render(request, 'catalog/student.html', context)
