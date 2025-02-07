# apps/kip_online_ru/models.py
from django.db import models

class Device(models.Model):
    name = models.CharField(max_length=255, verbose_name="Имя устройства")
    location = models.CharField(max_length=255, verbose_name="Расположение")
    status = models.CharField(max_length=50, verbose_name="Статус")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")

    def __str__(self):
        return self.name

class MonitoringData(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name="monitoring_data")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Время записи")
    parameter = models.CharField(max_length=100, verbose_name="Параметр")
    value = models.FloatField(verbose_name="Значение")

    def __str__(self):
        return f"{self.parameter} - {self.value} ({self.timestamp})"

class MQTTBrokerMessage(models.Model):
    id = models.AutoField(primary_key=True)
    client_id = models.CharField(max_length=255, verbose_name="ID клиента")
    topic = models.CharField(max_length=255, verbose_name="Топик")
    message = models.TextField(verbose_name="Сообщение")
    time_stamp = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")

    class Meta:
        db_table = "mqttbroker_tb"
        verbose_name = "Сообщение брокера MQTT"
        verbose_name_plural = "Сообщения брокера MQTT"

    def __str__(self):
        return f"{self.client_id} - {self.topic}"
