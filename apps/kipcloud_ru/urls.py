# kipclub/apps/kipcloud_ru/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_kc, name='cloud_home'),  # Главная страница для частных клиентов
    path('devices/', views.device_list_kc, name='cloud_device_list'),  # Список устройств
    path('device/<int:pk>/', views.device_detail_kc, name='cloud_device_detail'),  # Детали устройства
]
