from .models import CustomUser
from django.contrib.auth.backends import ModelBackend


class CustomUserAuth(ModelBackend):

    def authenticate(self, request, username=None, password=None):
        try:
            user = CustomUser.objects.get(email=username)
            if user.check_password(password):
                return user
        except CustomUser.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            user = CustomUser.objects.get(pk=user_id)
            if user.is_active:
                return user
        except CustomUser.DoesNotExist:
            return None
