import re

from rest_framework.permissions import BasePermission


class AuthPermission(BasePermission):
    EXCLUDED = ['/api/auth/token/', '/api/']

    def has_permission(self, request, view):
        public = any(re.match(r, request.path) for r in self.EXCLUDED)
        logged = request.user and request.user.is_authenticated

        return public or logged
