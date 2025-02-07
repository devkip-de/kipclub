from django.shortcuts import render, get_object_or_404
from .models import PrivateDevice

def home_kc(request):
    return render(request, 'home_kc.html')

def device_list_kc(request):
    devices = PrivateDevice.objects.all()
    return render(request, 'device_list_kc.html', {'devices': devices})

def device_detail_kc(request, pk):
    device = get_object_or_404(PrivateDevice, pk=pk)
    return render(request, 'device_detail_kc.html', {'device': device})
