from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Menu, Category
from django.core.exceptions import PermissionDenied

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

class MenuCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Menu
    fields = ['title', 'hook_text', 'content', 'head_image', 'price', 'category']

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated and (current_user.is_staff or current_user.is_superuser):
            form.instance.author = current_user
            return super(MenuCreate, self).form_valid(form)
        else:
            return redirect('/shop/')

class MenuUpdate(LoginRequiredMixin, UpdateView):
    model = Menu
    fields = ['title', 'hook_text', 'content', 'head_image', 'price', 'category']

    template_name = 'shop/menu_update_form.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(MenuUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

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