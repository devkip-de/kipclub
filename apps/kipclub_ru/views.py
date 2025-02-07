# apps/kipclub_ru/views.py
from django.shortcuts import render, redirect
from .forms import MQTTSettingsForm  # Импортируем форму для работы с настройками MQTT
from .models import MQTTSettings  # Импортируем модель настроек MQTT

# Главная страница сайта kipclub.ru
def home(request):
    return render(request, 'home.html')

# Представление для редактирования настроек MQTT
def mqtt_settings_view(request):
    # Получаем существующую запись настроек или создаём новую, если запись отсутствует
    mqtt_settings, created = MQTTSettings.objects.get_or_create(id=1)
    if request.method == "POST":
        # Если отправлен POST-запрос, обрабатываем данные формы
        form = MQTTSettingsForm(request.POST, instance=mqtt_settings)
        if form.is_valid():
            form.save()  # Сохраняем данные в базе
            return redirect("mqtt_settings_success")  # Перенаправляем на страницу успеха
    else:
        # Если GET-запрос, отображаем текущие данные в форме
        form = MQTTSettingsForm(instance=mqtt_settings)

    return render(request, "mqtt_settings.html", {"form": form})  # Отображаем страницу с формой

# Страница успешного сохранения настроек MQTT
def mqtt_settings_success(request):
    return render(request, "mqtt_settings_success.html")  # Сообщение об успешном сохранении
