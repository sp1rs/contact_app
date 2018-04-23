import base64

from django.contrib.auth import authenticate
from django.http import HttpResponse


def basic_auth():
    def decorator(func):
        def inner_func(request, *args, **kwargs):
            if 'HTTP_AUTHORIZATION' in request.META:
                auth = request.META['HTTP_AUTHORIZATION'].split()
                if len(auth) == 2:
                    # NOTE: We are only support basic authentication for now.
                    if auth[0].lower() == "basic":
                        username, password = base64.b64decode(auth[1]).split(':')
                        user = authenticate(username=username, password=password)
                        if user is not None:
                            if user.is_active:
                                request.user = user
                                return func(request, *args, **kwargs)
            response = HttpResponse()
            response.status_code = 401
            return response
        return inner_func
    return decorator
