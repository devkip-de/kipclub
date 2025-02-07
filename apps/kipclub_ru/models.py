# apps/kipclub_ru/models.py

from django.db import models

class MQTTSettings(models.Model):
    MQTT_BROKER = models.CharField(max_length=255, verbose_name="Брокер MQTT")
    MQTT_PORT = models.PositiveIntegerField(default=1883, verbose_name="Порт")
    MQTT_USERNAME = models.CharField(max_length=255, blank=True, null=True, verbose_name="Имя пользователя")
    MQTT_PASSWORD = models.CharField(max_length=255, blank=True, null=True, verbose_name="Пароль")
    MQTT_TOPICS = models.TextField(default="#", verbose_name="Топики (JSON)")
    ENCRYPTION = models.CharField(
        max_length=3,
        choices=(("yes", "Да"), ("no", "Нет")),
        default="no",
        verbose_name="Шифрование (SSL/TLS)"
    )

    def __str__(self):
        return f"{self.MQTT_BROKER}:{self.MQTT_PORT}"

