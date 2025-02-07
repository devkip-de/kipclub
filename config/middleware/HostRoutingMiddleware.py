# config/middleware/HostRoutingMiddleware.py
class HostRoutingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        host = request.get_host()

        # Если запрашивается /admin, используем стандартный URLconf
        if request.path.startswith('/admin'):
            request.urlconf = 'config.urls'
        elif host in ["kipclub.ru", "www.kipclub.ru"]:
            request.urlconf = "apps.kipclub_ru.urls"
        elif host in ["kipclub.store", "www.kipclub.store"]:
            request.urlconf = "apps.kipclub_store.urls"
        elif host in ["kip-online.ru", "www.kip-online.ru"]:
            request.urlconf = "apps.kip_online_ru.urls"
        elif host in ["kipcloud.ru", "www.kipcloud.ru"]:
            request.urlconf = "apps.kipcloud_ru.urls"
        else:
            from django.http import HttpResponseRedirect
            return HttpResponseRedirect("https://kipclub.ru")

        return self.get_response(request)


