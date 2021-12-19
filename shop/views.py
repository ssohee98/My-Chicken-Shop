from django.shortcuts import render
from .models import Menu

def index(request):
    menus = Menu.objects.all()

    return render(
        request,
        'shop/index.html',
        {
            'menus': menus,
        }
    )

def single_menu_page(request, pk):
    menu = Menu.objects.get(pk=pk)

    return render(
        request,
        'shop/single_menu_page.html',
        {
            'menu': menu,
        }
    )