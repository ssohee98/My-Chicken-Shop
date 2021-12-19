from django.urls import path
from . import views

urlpatterns = [
    path('delete_comment/<int:pk>/', views.delete_comment),
    path('update_comment/<int:pk>/', views.CommentUpdate.as_view()),
    path('update_menu/<int:pk>/', views.MenuUpdate.as_view()),
    path('create_menu/', views.MenuCreate.as_view()),
    path('category/<str:slug>/', views.category_page),
    path('<int:pk>/new_comment/', views.new_comment),
    path('<int:pk>/', views.MenuDetail.as_view()),
    path('', views.MenuList.as_view()),
    # path('<int:pk>/', views.single_menu_page),
    # path('', views.index),
]