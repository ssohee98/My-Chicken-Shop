from django.urls import path
from . import views

urlpatterns = [
    path('category/<str:slug>/', views.category_page),
    path('<int:pk>/', views.MenuDetail.as_view()),
    path('', views.MenuList.as_view()),
    # path('<int:pk>/', views.single_menu_page),
    # path('', views.index),
]