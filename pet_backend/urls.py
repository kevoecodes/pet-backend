from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # Authentications URLS
    path('api/auth/', include('users_management.urls.auth_urls')),

    # Users Resource URLs
    path('api/v1/', include('users_management.urls.urls')),
]
