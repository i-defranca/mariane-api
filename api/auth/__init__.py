from rest_framework_simplejwt.views import (
    TokenBlacklistView as TokenLogout,
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView as TokenLogin,
)
from rest_framework_simplejwt.views import (
    TokenRefreshView as TokenRefresh,
)

__all__ = ['TokenLogin', 'TokenLogout', 'TokenRefresh']
