from django.contrib import admin
from .models import PrivateDevice, PrivateMonitoringData

@admin.register(PrivateDevice)
class PrivateDeviceAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'location', 'status', 'created_at')
    search_fields = ('name', 'owner', 'location')

@admin.register(PrivateMonitoringData)
class PrivateMonitoringDataAdmin(admin.ModelAdmin):
    list_display = ('device', 'timestamp', 'parameter', 'value')
    list_filter = ('timestamp', 'parameter')