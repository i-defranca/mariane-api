import re

from django.conf import settings
from rest_framework import permissions
from rest_framework_simplejwt import authentication

PUBLIC_PATHS = settings.PUBLIC_PATHS


def public(request):
    return any(re.match(r, request.path) for r in PUBLIC_PATHS)


def authenticated(user):
    return user and user.is_authenticated


class OptionalAuth(authentication.JWTAuthentication):
    def authenticate(self, request):
        return None if public(request) else super().authenticate(request)


class DefaultPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return public(request) or authenticated(request.user)
