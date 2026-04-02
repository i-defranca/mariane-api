from rest_framework_simplejwt.views import (
    TokenBlacklistView as TokenLogout,
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView as TokenLogin,
)
from rest_framework_simplejwt.views import (
    TokenRefreshView as TokenRefresh,
)

from .views import AuthUserView as AuthUser

__all__ = ['AuthUser', 'TokenLogin', 'TokenLogout', 'TokenRefresh']
