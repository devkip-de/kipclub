# kipclub/apps/kip_online_ru/views.py
from django.shortcuts import render, get_object_or_404
from .forms import MqttMessageFilterForm
from .models import Device, MQTTBrokerMessage

def kol_home(request):
    return render(request, 'kol_home.html')

def device_list_kol(request):
    devices = Device.objects.all()
    return render(request, 'device_list_kol.html', {'devices': devices})

def device_detail_kol(request, pk):
    device = get_object_or_404(Device, pk=pk)
    return render(request, 'device_detail_kol.html', {'device': device})

# Представление для личного кабинета пользователя
def user_profile_view(request):
    return render(request, 'user_profile.html')


def mqtt_message_query(request):
    """Обрабатывает запрос формы и фильтрует данные из БД"""
    
    # Создаём экземпляр формы, если переданы параметры, заполняем форму
    form = MqttMessageFilterForm(request.GET or None)
    
    # Начинаем с выборки всех сообщений
    messages = MQTTBrokerMessage.objects.all()

    if form.is_valid():  # Проверяем корректность формы
        topic_root = form.cleaned_data.get("topic_root")  # Получаем корневой узел
        start_time = form.cleaned_data.get("start_time")  # Начало временного интервала
        end_time = form.cleaned_data.get("end_time")  # Конец временного интервала

        # Фильтруем по корневому узлу топика, если он задан
        if topic_root:
            messages = messages.filter(topic__startswith=topic_root)

        # Фильтруем по времени, если интервал задан
        if start_time and end_time:
            messages = messages.filter(time_stamp__range=(start_time, end_time))

    # Передаем форму и отфильтрованные сообщения в шаблон
    return render(request, "mqtt_message_query.html", {"form": form, "messages": messages})
