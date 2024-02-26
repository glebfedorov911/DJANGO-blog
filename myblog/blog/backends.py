from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend

from django.db.models import Q

class AuthBackend(BaseBackend):
    supports_objects_permissions = True
    supports_anonymous_user = True
    supports_inactive_user = False

    def authenticate(self, request, email=None, password=None, **kwargs):
        User = get_user_model()

        try:
            if email:
                user = User.objects.get(Q(email=email) | Q(phone=email))
            else:
                user = User.objects.get(Q(email=request.POST.get('username')) | Q(phone=request.POST.get('username')))
                password = request.POST.get('password')
        except User.DoesNotExist:
            return None

        return user if user.check_password(password) else None

    def get_user(self, user_id):
        User = get_user_model()

        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None