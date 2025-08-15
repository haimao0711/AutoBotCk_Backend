from rest_framework.response import Response
from rest_framework import status
from functools import wraps
from apps.authencation.user.models import User


def api_key_required(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        api_key = request.GET.get('api_key')

        if not api_key:
            return Response({'error': 'API key missing'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            user = User.objects.get(api_key=api_key)
        except User.DoesNotExist:
            return Response({'error': 'Invalid API key'}, status=status.HTTP_401_UNAUTHORIZED)

        request.user = user
        return func(request, *args, **kwargs)

    return wrapper
