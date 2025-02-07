from django.contrib import admin
from .models import Device, MonitoringData

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'status', 'created_at')
    search_fields = ('name', 'location')

@admin.register(MonitoringData)
class MonitoringDataAdmin(admin.ModelAdmin):
    list_display = ('device', 'timestamp', 'parameter', 'value')
    list_filter = ('timestamp', 'parameter')
    