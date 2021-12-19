from django.urls import path
from . import views

urlpatterns = [
    path('<int:pk>/', views.single_menu_page),
    path('', views.index),
]