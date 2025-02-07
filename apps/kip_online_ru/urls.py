# kipclub/apps/kip_online_ru/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.kol_home, name='online_home'),  # Главная страница мониторинга
    path('devices/', views.device_list_kol, name='online_device_list'),  # Список устройств
    path('device/<int:pk>/', views.device_detail_kol, name='online_device_detail'),  # Детали устройства
]
