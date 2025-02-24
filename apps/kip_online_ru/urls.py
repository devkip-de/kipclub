# kipclub/apps/kip_online_ru/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.kol_home, name='online_home'),  # Главная страница мониторинга
    path('devices/', views.device_list_kol, name='online_device_list'),  # Список устройств
    path('device/<int:pk>/', views.device_detail_kol, name='online_device_detail'),  # Детали устройства
    path('user-profile/', views.user_profile_view, name='user_profile'),  # Новый маршрут для личного кабинета
    path('mqtt_message_query/', views.mqtt_message_query, name='mqtt_message_query'),   # URL-адрес для страницы с формой запроса и выборкой данных
]
