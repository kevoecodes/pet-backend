from django.urls import path

from users_management.views import LoginUser, ResetUserPassword

urlpatterns = [
    path('login', LoginUser.as_view(), name='login-user'),
    path('reset-password/<str:pk>', ResetUserPassword.as_view(), name='reset-password'),
]
