from django.core.exceptions import PermissionDenied


def user_is_master(function):
    def wrap(request, *args, **kwargs):
        user = request.user
        if user.user_type == "master":
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


def user_is_student(function):
    def wrap(request, *args, **kwargs):
        user = request.user
        if user.user_type == "Others":
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap