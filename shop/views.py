from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Menu

class MenuList(ListView):
    model = Menu

class MenuDetail(DetailView):
    model = Menu

# def index(request):
#     posts = Post.objects.all().order_by('-pk')
#
#     return render(
#         request,
#         'blog/menu_list.html',
#         {
#             'posts': posts,
#         }
#     )

# def single_menu_page(request, pk):
#     menu = Menu.objects.get(pk=pk)
#
#     return render(
#         request,
#         'shop/menu_detail.html',
#         {
#             'menu': menu,
#         }
#     )