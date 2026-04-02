from django.urls import path

from api.auth import AuthUser, TokenLogin, TokenLogout, TokenRefresh

urlpatterns = [
    path('token/login/', TokenLogin.as_view(), name='t_login'),
    path('token/refresh/', TokenRefresh.as_view(), name='t_refresh'),
    path('token/logout/', TokenLogout.as_view(), name='t_logout'),
    path('user/', AuthUser.as_view(), name='auth_user'),
]
