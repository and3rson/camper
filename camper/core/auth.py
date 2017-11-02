from django.contrib.auth.models import User
from rest_framework import authentication
from rest_framework import exceptions


class PlainAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        method, _, payload = request.META.get('HTTP_AUTHORIZATION', '').partition(' ')
        if method.lower() != 'plain':
            return None
        username, _, password = payload.partition(':')
        if not username or not password:
            return None

        user = User.objects.filter(username=username).first()
        if not user:
            raise exceptions.AuthenticationFailed('Username not found.')

        if not user.check_password(password):
            raise exceptions.AuthenticationFailed('Wrong password.')

        return (user, None)

