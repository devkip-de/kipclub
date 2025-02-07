from django.db import models

class PrivateDevice(models.Model):
    name = models.CharField(max_length=255, verbose_name="Имя устройства")
    owner = models.CharField(max_length=255, verbose_name="Владелец")
    location = models.CharField(max_length=255, verbose_name="Расположение")
    status = models.CharField(max_length=50, verbose_name="Статус")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")

    def __str__(self):
        return f"{self.name} - {self.owner}"

class PrivateMonitoringData(models.Model):
    device = models.ForeignKey(PrivateDevice, on_delete=models.CASCADE, related_name="monitoring_data")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Время записи")
    parameter = models.CharField(max_length=100, verbose_name="Параметр")
    value = models.FloatField(verbose_name="Значение")

    def __str__(self):
        return f"{self.parameter} - {self.value} ({self.timestamp})"
