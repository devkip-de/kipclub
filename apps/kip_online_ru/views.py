from django.shortcuts import render, get_object_or_404
from .models import Device

def kol_home(request):
    return render(request, 'kol_home.html')

def device_list_kol(request):
    devices = Device.objects.all()
    return render(request, 'device_list_kol.html', {'devices': devices})

def device_detail_kol(request, pk):
    device = get_object_or_404(Device, pk=pk)
    return render(request, 'device_detail_kol.html', {'device': device})