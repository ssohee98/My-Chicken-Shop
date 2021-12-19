from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Menu, Category

class MenuList(ListView):
    model = Menu

    def get_context_data(self, **kwargs):
        context = super(MenuList, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_menu_count'] = Menu.objects.filter(category=None).count()
        return context

class MenuDetail(DetailView):
    model = Menu

    def get_context_data(self, **kwargs):
        context = super(MenuDetail, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_menu_count'] = Menu.objects.filter(category=None).count()
        return context

def category_page(request, slug):
    if slug == 'no_category':
        category = '미분류'
        menu_list = Menu.objects.filter(category=None)
    else:
        category = Category.objects.get(slug=slug)
        menu_list = Menu.objects.filter(category=category)

    return render(
        request,
        'shop/menu_list.html',
        {
            'menu_list': menu_list,
            'categories': Category.objects.all(),
            'no_category_menu_count': Menu.objects.filter(category=None).count(),
            'category': category,
        }
    )
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