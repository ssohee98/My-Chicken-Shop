from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404
from .models import Menu, Category, Comment
from django.core.exceptions import PermissionDenied
from .forms import CommentForm


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
        context['comment_form'] = CommentForm
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


def new_comment(request, pk):
    if request.user.is_authenticated:
        menu = get_object_or_404(Menu, pk=pk)

        if request.method == 'POST':
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.menu = menu
                comment.author = request.user
                comment.save()
                return redirect(comment.get_absolute_url())
        else:
            return redirect(menu.get_absolute_url())
    else:
        raise PermissionDenied

def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    menu = comment.menu
    if request.user.is_authenticated and request.user == comment.author:
        comment.delete()
        return redirect(menu.get_absolute_url())
    else:
        raise PermissionDenied

class CommentUpdate(LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(CommentUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

