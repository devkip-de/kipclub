# apps/kip_online_ru/forms.py
from django import forms

class MqttMessageFilterForm(forms.Form):
    topic_root = forms.CharField(required=False, label="Корневой узел топика", max_length=255)
    start_time = forms.DateTimeField(required=False, label="Время начала", widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    end_time = forms.DateTimeField(required=False, label="Время окончания", widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))

