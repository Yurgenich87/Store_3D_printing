from django.http import HttpResponseRedirect
from django.urls import reverse

class AdminRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith(reverse('admin:index')):
            if not request.user.is_admin:
                return HttpResponseRedirect(reverse('index'))
        return self.get_response(request)
