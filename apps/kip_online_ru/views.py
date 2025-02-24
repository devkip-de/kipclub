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

def user_profile_view(request):
    return render(request, 'user_profile.html')

def mqtt_message_query(request):
    """Обрабатывает запрос формы и фильтрует данные из БД"""
    
    # Если нажата кнопка "Очистить фильтр", сбрасываем параметры
    if "clear_filter" in request.GET:
        form = MqttMessageFilterForm()  # Создаем пустую форму
        messages = MQTTBrokerMessage.objects.all()  # Все сообщения без фильтров
    else:
        form = MqttMessageFilterForm(request.GET or None)
        messages = MQTTBrokerMessage.objects.all()

        if form.is_valid():
            topic_root = form.cleaned_data.get("topic_root")
            start_time = form.cleaned_data.get("start_time")
            end_time = form.cleaned_data.get("end_time")

            if topic_root:
                messages = messages.filter(topic__startswith=topic_root)

            if start_time and end_time:
                messages = messages.filter(time_stamp__range=(start_time, end_time))

    return render(request, "mqtt_message_query.html", {"form": form, "messages": messages})
