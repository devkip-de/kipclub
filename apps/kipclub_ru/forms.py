# apps/kipclub_ru/forms.py

from django import forms
from .models import MQTTSettings

class MQTTSettingsForm(forms.ModelForm):
    class Meta:
        model = MQTTSettings
        fields = ["MQTT_BROKER", "MQTT_PORT", "MQTT_USERNAME", "MQTT_PASSWORD", "MQTT_TOPICS", "ENCRYPTION"]
        widgets = {
            "MQTT_TOPICS": forms.Textarea(attrs={"rows": 3, "cols": 50}),
            "MQTT_PASSWORD": forms.PasswordInput(render_value=True),
        }
        labels = {
            "MQTT_BROKER": "Брокер MQTT",
            "MQTT_PORT": "Порт",
            "MQTT_USERNAME": "Имя пользователя",
            "MQTT_PASSWORD": "Пароль",
            "MQTT_TOPICS": "Топики (в JSON формате)",
            "ENCRYPTION": "Шифрование SSL/TLS",
        }
