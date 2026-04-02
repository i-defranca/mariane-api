from django.urls import include, path

from api.auth.urls import urlpatterns as auth_urls
from api.routers import router

urlpatterns = [
    path('auth/', include(auth_urls)),
    path('', include(router.urls)),
]
