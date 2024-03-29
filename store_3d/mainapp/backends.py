from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model

from store_3d.mainapp.models import User

UserModel = get_user_model()


class EmailBackend(BaseBackend):
    """Custom authentication backend to authenticate users via email"""

    def authenticate(self, request, email=None, password=None):
        """Authenticate users using email and password"""
        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        """Retrieve user by user ID"""
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
