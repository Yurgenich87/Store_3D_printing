from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import redirect, render
from django.urls import reverse


class AdminRedirectMiddleware:
    """Middleware to redirect unauthorized users from admin pages."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        """Handle incoming requests."""
        if request.path.startswith(reverse('admin:index')):
            if not request.user.is_admin:
                return self.handle_forbidden_request(request)

        return self.get_response(request)

    def handle_forbidden_request(self, request):
        """Handle forbidden request."""
        message = "Access is restricted. Please contact the administrator."
        return render(request, 'mainapp/forbidden.html', {'message': message})
