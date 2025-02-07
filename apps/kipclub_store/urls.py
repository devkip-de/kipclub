# kipclub/apps/kipclub_store/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_store, name='home'),  # Установите 'home' как имя маршрута
    path('product/', views.product_list, name='product_list'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
]
