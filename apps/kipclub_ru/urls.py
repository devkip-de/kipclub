# apps/kipclub_ru/urls.py
from django.urls import path
from . import views  # Импортируем представления из текущего приложения

urlpatterns = [
    path('', views.home, name='home'),  # Главная страница сайта kipclub.ru
    path('mqtt-settings/', views.mqtt_settings_view, name='mqtt_settings'),  # Страница настроек MQTT
    path('mqtt-settings/success/', views.mqtt_settings_success, name='mqtt_settings_success'),  # Страница успеха
]
